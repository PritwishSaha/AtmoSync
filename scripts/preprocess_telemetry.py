import pandas as pd
from pathlib import Path


# ============================================================
# AtmoSync - Day 5
# Telemetry Preprocessing & Feature Engineering
# ============================================================

INPUT_FILE = Path("data/validated/validated_telemetry.csv")
OUTPUT_FILE = Path("data/processed/iot_telemetry_features.csv")


def load_data():
    """Load validated telemetry data."""
    print("\n[1] Loading validated telemetry...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Rows loaded: {len(df)}")
    print(f"Columns loaded: {len(df.columns)}")

    return df


def create_timestamp_features(df):
    """Create useful time-based features."""

    print("\n[2] Creating timestamp features...")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["day_name"] = df["timestamp"].dt.day_name()

    return df


def create_temperature_features(df):
    """Create temperature-related features."""

    print("\n[3] Creating temperature features...")

    df["temperature_deviation"] = abs(df["temperature"] - 10)

    df["temperature_risk"] = pd.cut(
        df["temperature"],
        bins=[-float("inf"), 5, 15, 20, float("inf")],
        labels=["LOW", "NORMAL", "WARNING", "CRITICAL"]
    )

    return df


def create_humidity_features(df):
    """Create humidity-related features."""

    print("\n[4] Creating humidity features...")

    df["humidity_risk"] = pd.cut(
        df["humidity"],
        bins=[-float("inf"), 70, 90, 95, float("inf")],
        labels=["LOW", "NORMAL", "WARNING", "CRITICAL"]
    )

    return df


def create_vibration_features(df):
    """Create vibration-related features."""

    print("\n[5] Creating vibration features...")

    df["vibration_risk"] = pd.cut(
        df["vibration"],
        bins=[-float("inf"), 0.20, 0.40, 0.60, float("inf")],
        labels=["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    )

    return df


def create_environmental_risk(df):
    """Calculate combined environmental risk score."""

    print("\n[6] Creating environmental risk score...")

    temperature_score = pd.cut(
        df["temperature"],
        bins=[-float("inf"), 5, 15, 20, float("inf")],
        labels=[0, 1, 2, 3]
    ).astype(int)

    humidity_score = pd.cut(
        df["humidity"],
        bins=[-float("inf"), 70, 90, 95, float("inf")],
        labels=[0, 1, 2, 3]
    ).astype(int)

    vibration_score = pd.cut(
        df["vibration"],
        bins=[-float("inf"), 0.20, 0.40, 0.60, float("inf")],
        labels=[0, 1, 2, 3]
    ).astype(int)

    df["environmental_risk_score"] = (
        temperature_score
        + humidity_score
        + vibration_score
    )

    df["environmental_risk"] = pd.cut(
        df["environmental_risk_score"],
        bins=[-1, 2, 4, 6, float("inf")],
        labels=["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    )

    return df


def create_spoilage_risk(df):
    """Create a simple spoilage-risk indicator."""

    print("\n[7] Creating spoilage risk...")

    df["spoilage_risk"] = "LOW"

    df.loc[
        df["environmental_risk_score"] >= 3,
        "spoilage_risk"
    ] = "MEDIUM"

    df.loc[
        df["environmental_risk_score"] >= 5,
        "spoilage_risk"
    ] = "HIGH"

    df.loc[
        df["environmental_risk_score"] >= 7,
        "spoilage_risk"
    ] = "CRITICAL"

    return df


def create_container_statistics(df):
    """Create container-level statistics."""

    print("\n[8] Creating container-level statistics...")

    container_stats = (
        df.groupby("container_id")
        .agg(
            avg_temperature=("temperature", "mean"),
            max_temperature=("temperature", "max"),
            min_temperature=("temperature", "min"),
            avg_humidity=("humidity", "mean"),
            max_humidity=("humidity", "max"),
            min_humidity=("humidity", "min"),
            avg_vibration=("vibration", "mean"),
            max_vibration=("vibration", "max"),
            warning_count=("condition", lambda x: (x == "WARNING").sum()),
            anomaly_count=("condition", lambda x: (x == "ANOMALY").sum()),
            avg_environmental_risk=("environmental_risk_score", "mean")
        )
        .reset_index()
    )

    df = df.merge(
        container_stats,
        on="container_id",
        how="left"
    )

    return df


def create_commodity_statistics(df):
    """Create commodity-level statistics."""

    print("\n[9] Creating commodity-level statistics...")

    commodity_stats = (
        df.groupby("commodity")
        .agg(
            commodity_avg_temperature=("temperature", "mean"),
            commodity_avg_humidity=("humidity", "mean"),
            commodity_avg_vibration=("vibration", "mean"),
            commodity_warning_count=("condition", lambda x: (x == "WARNING").sum()),
            commodity_anomaly_count=("condition", lambda x: (x == "ANOMALY").sum()),
            commodity_avg_risk=("environmental_risk_score", "mean")
        )
        .reset_index()
    )

    df = df.merge(
        commodity_stats,
        on="commodity",
        how="left"
    )

    return df


def save_data(df):
    """Save processed dataset."""

    print("\n[10] Saving processed dataset...")

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Output saved to: {OUTPUT_FILE}")
    print(f"Final rows: {len(df)}")
    print(f"Final columns: {len(df.columns)}")


def main():

    print("=" * 60)
    print("AtmoSync - Day 5 Telemetry Preprocessing")
    print("=" * 60)

    df = load_data()

    df = create_timestamp_features(df)
    df = create_temperature_features(df)
    df = create_humidity_features(df)
    df = create_vibration_features(df)
    df = create_environmental_risk(df)
    df = create_spoilage_risk(df)
    df = create_container_statistics(df)
    df = create_commodity_statistics(df)

    save_data(df)

    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()