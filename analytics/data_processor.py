import pandas as pd
from pathlib import Path

from commodity_rules import COMMODITY_RULES


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "iot_telemetry.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "iot_telemetry_cleaned.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("ATMOSYNC - DATA PROCESSING")
print("=" * 60)

print("\nLoading IoT telemetry...")

df = pd.read_csv(RAW_FILE)

print(f"Rows loaded: {len(df)}")


# ============================================================
# BASIC CLEANING
# ============================================================

df = df.drop_duplicates()

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

numeric_columns = [
    "temperature",
    "humidity",
    "vibration"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# Remove invalid required records
df = df.dropna(
    subset=[
        "container_id",
        "timestamp",
        "commodity",
        "temperature",
        "humidity",
        "vibration",
        "condition"
    ]
)


# ============================================================
# TIME FEATURES
# ============================================================

df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour
df["minute"] = df["timestamp"].dt.minute


# ============================================================
# COMMODITY-SPECIFIC RULES
# ============================================================

df["temperature_min"] = df["commodity"].map(
    lambda x: COMMODITY_RULES[x]["temperature_min"]
)

df["temperature_max"] = df["commodity"].map(
    lambda x: COMMODITY_RULES[x]["temperature_max"]
)

df["humidity_min"] = df["commodity"].map(
    lambda x: COMMODITY_RULES[x]["humidity_min"]
)

df["humidity_max"] = df["commodity"].map(
    lambda x: COMMODITY_RULES[x]["humidity_max"]
)


# ============================================================
# TEMPERATURE DEVIATION
# ============================================================

def calculate_temperature_deviation(row):

    temperature = row["temperature"]

    if temperature < row["temperature_min"]:
        return round(
            row["temperature_min"] - temperature,
            2
        )

    elif temperature > row["temperature_max"]:
        return round(
            temperature - row["temperature_max"],
            2
        )

    return 0.0


df["temperature_deviation"] = df.apply(
    calculate_temperature_deviation,
    axis=1
)


# ============================================================
# HUMIDITY DEVIATION
# ============================================================

def calculate_humidity_deviation(row):

    humidity = row["humidity"]

    if humidity < row["humidity_min"]:
        return round(
            row["humidity_min"] - humidity,
            2
        )

    elif humidity > row["humidity_max"]:
        return round(
            humidity - row["humidity_max"],
            2
        )

    return 0.0


df["humidity_deviation"] = df.apply(
    calculate_humidity_deviation,
    axis=1
)


# ============================================================
# RISK COMPONENTS
# ============================================================

df["temperature_risk_score"] = (
    df["temperature_deviation"] / 5
).clip(0, 1)


df["humidity_risk_score"] = (
    df["humidity_deviation"] / 20
).clip(0, 1)


df["vibration_risk_score"] = (
    (df["vibration"] - 0.20) / 0.40
).clip(0, 1)


# ============================================================
# OVERALL RISK SCORE
# ============================================================

df["microclimate_risk_score"] = (
    df["temperature_risk_score"] * 0.40
    +
    df["humidity_risk_score"] * 0.35
    +
    df["vibration_risk_score"] * 0.25
)


df["microclimate_risk_score"] = (
    df["microclimate_risk_score"] * 100
).round(2)


# ============================================================
# RISK CATEGORY
# ============================================================

def classify_risk(score):

    if score < 25:
        return "Low"

    elif score < 60:
        return "Medium"

    elif score < 80:
        return "High"

    return "Critical"


df["microclimate_risk"] = (
    df["microclimate_risk_score"]
    .apply(classify_risk)
)


# ============================================================
# EXCURSION FLAGS
# ============================================================

df["temperature_excursion"] = (
    df["temperature_deviation"] > 0
)

df["humidity_excursion"] = (
    df["humidity_deviation"] > 0
)

df["vibration_anomaly"] = (
    df["vibration"] > 0.35
)


# ============================================================
# SAVE
# ============================================================

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\nProcessing completed successfully.")

print(f"Final rows: {len(df)}")

print(f"Final columns: {len(df.columns)}")

print("\nRisk distribution:")

print(
    df["microclimate_risk"]
    .value_counts()
)


print("\nRisk by container:")

print(
    df.groupby("container_id")[
        "microclimate_risk_score"
    ]
    .mean()
    .sort_values(ascending=False)
)


print("\nRisk by commodity:")

print(
    df.groupby("commodity")[
        "microclimate_risk_score"
    ]
    .mean()
    .sort_values(ascending=False)
)


print("\nOutput:")

print(OUTPUT_FILE)

print("\n" + "=" * 60)
print("DATA PROCESSING COMPLETED")
print("=" * 60)