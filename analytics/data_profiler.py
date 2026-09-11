import pandas as pd
from pathlib import Path


# =========================
# Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "processed" / "iot_telemetry_cleaned.csv"


# =========================
# Load processed data
# =========================

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("ATMOSYNC - DATA PROFILING")
print("=" * 60)

print(f"\nTotal rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")


# =========================
# Dataset information
# =========================

print("\n--- DATA TYPES ---")
print(df.dtypes)


# =========================
# Missing values
# =========================

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())


# =========================
# Duplicate records
# =========================

print("\n--- DUPLICATES ---")
print("Duplicate rows:", df.duplicated().sum())


# =========================
# Container analysis
# =========================

print("\n--- CONTAINERS ---")
print("Number of containers:", df["container_id"].nunique())

print("\nRecords per container:")
print(df["container_id"].value_counts())


# =========================
# Commodity analysis
# =========================

print("\n--- COMMODITIES ---")
print("Number of commodities:", df["commodity"].nunique())

print("\nRecords per commodity:")
print(df["commodity"].value_counts())


# =========================
# Numerical statistics
# =========================

numeric_columns = [
    "temperature",
    "humidity",
    "vibration",
    "temperature_deviation",
    "humidity_deviation",
    "microclimate_risk_score"
]

print("\n--- NUMERICAL SUMMARY ---")
print(df[numeric_columns].describe())


# =========================
# Risk analysis
# =========================

print("\n--- TEMPERATURE RISK ---")
print(df["temperature_risk"].value_counts())


print("\n--- HUMIDITY RISK ---")
print(df["humidity_risk"].value_counts())


print("\n--- VIBRATION RISK ---")
print(df["vibration_risk"].value_counts())


print("\n--- MICROCLIMATE RISK ---")
print(df["microclimate_risk"].value_counts())


# =========================
# High-risk records
# =========================

high_risk = df[df["microclimate_risk"] == "High"]

print("\n--- HIGH-RISK RECORDS ---")
print("High-risk records:", len(high_risk))

if len(high_risk) > 0:
    print(
        high_risk[
            [
                "container_id",
                "commodity",
                "temperature",
                "humidity",
                "vibration",
                "microclimate_risk"
            ]
        ].head(10)
    )


# =========================
# Container risk
# =========================

print("\n--- RISK BY CONTAINER ---")

container_risk = (
    df.groupby("container_id", observed=True)["microclimate_risk_score"]
    .mean()
    .sort_values(ascending=False)
)

print(container_risk)


# =========================
# Commodity risk
# =========================

print("\n--- RISK BY COMMODITY ---")

commodity_risk = (
    df.groupby("commodity", observed=True)["microclimate_risk_score"]
    .mean()
    .sort_values(ascending=False)
)

print(commodity_risk)


print("\n" + "=" * 60)
print("DATA PROFILING COMPLETED")
print("=" * 60)