import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# AtmoSync - Spoilage Risk Engine
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "iot_telemetry_cleaned.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "iot_telemetry_spoilage.csv"

print("=" * 60)
print("ATMOSYNC - SPOILAGE RISK ENGINE")
print("=" * 60)

# ---------------------------------------------------------
# Load processed telemetry
# ---------------------------------------------------------

print("\nLoading processed telemetry...")

df = pd.read_csv(INPUT_FILE)

print(f"Rows loaded: {len(df)}")

# ---------------------------------------------------------
# Sort telemetry chronologically
# ---------------------------------------------------------

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

df = df.sort_values(
    ["container_id", "timestamp"]
).reset_index(drop=True)

# ---------------------------------------------------------
# Calculate exposure duration
# ---------------------------------------------------------
# Each sensor record represents the period until the
# next reading from the same container.
#
# Maximum exposure interval is capped at 10 minutes
# to avoid unrealistic gaps affecting the score.

df["next_timestamp"] = (
    df.groupby("container_id")["timestamp"]
    .shift(-1)
)

df["exposure_minutes"] = (
    df["next_timestamp"] - df["timestamp"]
).dt.total_seconds() / 60

df["exposure_minutes"] = (
    df["exposure_minutes"]
    .fillna(2)
    .clip(lower=0, upper=10)
)

# ---------------------------------------------------------
# Exposure multiplier
# ---------------------------------------------------------
# Longer exposure increases spoilage risk.

df["exposure_multiplier"] = (
    df["exposure_minutes"] / 10
).clip(0, 1)

# ---------------------------------------------------------
# Microclimate severity
# ---------------------------------------------------------

df["microclimate_severity"] = (
    df["microclimate_risk_score"] / 100
)

# ---------------------------------------------------------
# Excursion severity
# ---------------------------------------------------------

df["temperature_severity"] = (
    df["temperature_risk_score"]
)

df["humidity_severity"] = (
    df["humidity_risk_score"]
)

df["vibration_severity"] = (
    df["vibration_risk_score"]
)

# ---------------------------------------------------------
# Spoilage Risk Score
# ---------------------------------------------------------
# Weighted analytical model:
#
# Microclimate severity : 45%
# Temperature severity  : 20%
# Humidity severity     : 15%
# Vibration severity    : 10%
# Exposure duration     : 10%
#
# These are project-level analytical assumptions.

df["spoilage_risk_score"] = (
    df["microclimate_severity"] * 0.45
    + df["temperature_severity"] * 0.20
    + df["humidity_severity"] * 0.15
    + df["vibration_severity"] * 0.10
    + df["exposure_multiplier"] * 0.10
) * 100

df["spoilage_risk_score"] = (
    df["spoilage_risk_score"]
    .clip(0, 100)
    .round(2)
)

# ---------------------------------------------------------
# Spoilage Risk Classification
# ---------------------------------------------------------

def classify_spoilage(score):
    if score < 25:
        return "Low"
    elif score < 60:
        return "Medium"
    elif score < 80:
        return "High"
    return "Critical"


df["spoilage_risk"] = (
    df["spoilage_risk_score"]
    .apply(classify_spoilage)
)

# ---------------------------------------------------------
# Spoilage Flag
# ---------------------------------------------------------

df["spoilage_flag"] = (
    df["spoilage_risk_score"] >= 60
)

# ---------------------------------------------------------
# Remove helper column
# ---------------------------------------------------------

df = df.drop(columns=["next_timestamp"])

# ---------------------------------------------------------
# Save output
# ---------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

print("\nSpoilage risk calculation completed.")

print(f"\nFinal rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")

print("\nSpoilage Risk Distribution:")
print(
    df["spoilage_risk"]
    .value_counts()
)

print("\nSpoilage Risk by Condition:")
print(
    pd.crosstab(
        df["condition"],
        df["spoilage_risk"]
    )
)

print("\nAverage Spoilage Risk by Commodity:")
print(
    df.groupby("commodity")["spoilage_risk_score"]
    .mean()
    .sort_values(ascending=False)
    .round(2)
)

print("\nTop 10 Spoilage Risk Records:")

columns = [
    "container_id",
    "commodity",
    "temperature",
    "humidity",
    "vibration",
    "condition",
    "microclimate_risk_score",
    "spoilage_risk_score",
    "spoilage_risk",
    "spoilage_flag"
]

print(
    df.nlargest(
        10,
        "spoilage_risk_score"
    )[columns].to_string(index=False)
)

print("\nOutput:")
print(OUTPUT_FILE)

print("\n" + "=" * 60)
print("SPOILAGE RISK ENGINE COMPLETED")
print("=" * 60)