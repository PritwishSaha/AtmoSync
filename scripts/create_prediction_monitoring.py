import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "ml_predictions.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "prediction_monitoring.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("Input dataset shape:", df.shape)


# ============================================================
# CONFIDENCE CATEGORY
# ============================================================

def confidence_category(confidence):

    if confidence >= 0.90:
        return "HIGH CONFIDENCE"

    elif confidence >= 0.75:
        return "MEDIUM CONFIDENCE"

    else:
        return "LOW CONFIDENCE"


df["confidence_category"] = (
    df["prediction_confidence"]
    .apply(confidence_category)
)


# ============================================================
# PREDICTION STATUS
# ============================================================

df["prediction_status"] = df.apply(
    lambda row:
        "CORRECT"
        if row["condition"] == row["predicted_condition"]
        else "INCORRECT",
    axis=1
)


# ============================================================
# MONITORING LEVEL
# ============================================================

def monitoring_level(row):

    if row["predicted_condition"] == "ANOMALY":

        if row["prediction_confidence"] < 0.90:
            return "HIGH PRIORITY REVIEW"

        return "ANOMALY DETECTED"

    if row["confidence_category"] == "LOW CONFIDENCE":
        return "REVIEW REQUIRED"

    if row["predicted_condition"] == "WARNING":
        return "MONITOR"

    return "NORMAL"


df["monitoring_level"] = df.apply(
    monitoring_level,
    axis=1
)


# ============================================================
# SELECT IMPORTANT COLUMNS
# ============================================================

monitoring_columns = [
    "container_id",
    "timestamp",
    "commodity",
    "temperature",
    "humidity",
    "vibration",
    "condition",
    "predicted_condition",
    "prediction_confidence",
    "confidence_category",
    "prediction_status",
    "monitoring_level"
]

monitoring_df = df[monitoring_columns].copy()


# ============================================================
# SAVE
# ============================================================

monitoring_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\nPrediction Status:")
print(
    monitoring_df["prediction_status"]
    .value_counts()
)


print("\nConfidence Category:")
print(
    monitoring_df["confidence_category"]
    .value_counts()
)


print("\nMonitoring Level:")
print(
    monitoring_df["monitoring_level"]
    .value_counts()
)


print("\nPredicted Condition:")
print(
    monitoring_df["predicted_condition"]
    .value_counts()
)


print("\nOutput shape:", monitoring_df.shape)

print("\nSaved to:")
print(OUTPUT_FILE)