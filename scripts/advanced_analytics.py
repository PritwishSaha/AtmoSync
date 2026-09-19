from pathlib import Path

import pandas as pd


# ============================================================
# AtmoSync — Day 12 Advanced Analytics
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


TELEMETRY_FILE = PROCESSED_DIR / "iot_telemetry_features.csv"
PREDICTION_FILE = PROCESSED_DIR / "prediction_monitoring.csv"
ARBITRAGE_FILE = PROCESSED_DIR / "arbitrage_decisions.csv"

OUTPUT_FILE = PROCESSED_DIR / "advanced_analytics.csv"


def load_data():
    """Load the processed AtmoSync datasets."""

    telemetry = pd.read_csv(TELEMETRY_FILE)
    predictions = pd.read_csv(PREDICTION_FILE)
    arbitrage = pd.read_csv(ARBITRAGE_FILE)

    return telemetry, predictions, arbitrage


def prepare_data(telemetry, predictions, arbitrage):
    """Prepare common analytical columns."""

    telemetry["timestamp"] = pd.to_datetime(
        telemetry["timestamp"],
        errors="coerce"
    )

    predictions["timestamp"] = pd.to_datetime(
        predictions["timestamp"],
        errors="coerce"
    )

    arbitrage["timestamp"] = pd.to_datetime(
        arbitrage["timestamp"],
        errors="coerce"
    )

    # Select prediction columns needed for analysis.
    prediction_columns = [
        "container_id",
        "timestamp",
        "commodity",
        "predicted_condition",
        "prediction_confidence",
    ]

    available_prediction_columns = [
        col for col in prediction_columns
        if col in predictions.columns
    ]

    predictions_small = predictions[available_prediction_columns].copy()

    # Merge prediction information with telemetry features.
    merged = telemetry.merge(
        predictions_small,
        on=["container_id", "timestamp", "commodity"],
        how="left",
        suffixes=("", "_prediction"),
    )

    # Add arbitrage action if available.
    arbitrage_columns = [
        "container_id",
        "timestamp",
        "commodity",
        "recommended_action",
        "arbitrage_opportunity",
    ]

    available_arbitrage_columns = [
        col for col in arbitrage_columns
        if col in arbitrage.columns
    ]

    arbitrage_small = arbitrage[available_arbitrage_columns].copy()

    merged = merged.merge(
        arbitrage_small,
        on=["container_id", "timestamp", "commodity"],
        how="left",
        suffixes=("", "_arbitrage"),
    )

    # Time features.
    merged["hour"] = merged["timestamp"].dt.hour
    merged["date"] = merged["timestamp"].dt.date
    merged["day_of_week"] = merged["timestamp"].dt.day_name()

    # Numerical safety.
    for column in [
        "temperature",
        "humidity",
        "vibration",
        "environmental_risk_score",
        "prediction_confidence",
    ]:
        if column in merged.columns:
            merged[column] = pd.to_numeric(
                merged[column],
                errors="coerce"
            )

    return merged


def create_container_profile(df):
    """Create container-level risk profile."""

    grouped = df.groupby("container_id")

    profile = grouped.agg(
        total_records=("container_id", "size"),
        anomaly_records=(
            "predicted_condition",
            lambda x: (x.astype(str).str.upper() == "ANOMALY").sum(),
        ),
        warning_records=(
            "predicted_condition",
            lambda x: (x.astype(str).str.upper() == "WARNING").sum(),
        ),
        high_risk_records=(
            "spoilage_risk",
            lambda x: x.astype(str).str.upper().eq("HIGH").sum(),
        ),
        critical_risk_records=(
            "spoilage_risk",
            lambda x: x.astype(str).str.upper().eq("CRITICAL").sum(),
        ),
        avg_temperature=("temperature", "mean"),
        avg_humidity=("humidity", "mean"),
        avg_vibration=("vibration", "mean"),
        avg_environmental_risk=(
            "environmental_risk_score",
            "mean",
        ),
    ).reset_index()

    profile["anomaly_rate_pct"] = (
        profile["anomaly_records"]
        / profile["total_records"]
        * 100
    )

    profile["high_critical_rate_pct"] = (
        (
            profile["high_risk_records"]
            + profile["critical_risk_records"]
        )
        / profile["total_records"]
        * 100
    )

    return profile


def create_commodity_profile(df):
    """Create commodity-level risk profile."""

    grouped = df.groupby("commodity")

    profile = grouped.agg(
        total_records=("commodity", "size"),
        anomaly_records=(
            "predicted_condition",
            lambda x: (x.astype(str).str.upper() == "ANOMALY").sum(),
        ),
        warning_records=(
            "predicted_condition",
            lambda x: (x.astype(str).str.upper() == "WARNING").sum(),
        ),
        high_risk_records=(
            "spoilage_risk",
            lambda x: x.astype(str).str.upper().eq("HIGH").sum(),
        ),
        critical_risk_records=(
            "spoilage_risk",
            lambda x: x.astype(str).str.upper().eq("CRITICAL").sum(),
        ),
        avg_temperature=("temperature", "mean"),
        avg_humidity=("humidity", "mean"),
        avg_vibration=("vibration", "mean"),
        avg_environmental_risk=(
            "environmental_risk_score",
            "mean",
        ),
    ).reset_index()

    profile["anomaly_rate_pct"] = (
        profile["anomaly_records"]
        / profile["total_records"]
        * 100
    )

    profile["high_critical_rate_pct"] = (
        (
            profile["high_risk_records"]
            + profile["critical_risk_records"]
        )
        / profile["total_records"]
        * 100
    )

    return profile


def create_hourly_profile(df):
    """Analyze risk and anomalies by hour."""

    grouped = df.groupby("hour")

    profile = grouped.agg(
        total_records=("hour", "size"),
        anomaly_records=(
            "predicted_condition",
            lambda x: (x.astype(str).str.upper() == "ANOMALY").sum(),
        ),
        high_critical_records=(
            "spoilage_risk",
            lambda x: x.astype(str).str.upper().isin(
                ["HIGH", "CRITICAL"]
            ).sum(),
        ),
        avg_temperature=("temperature", "mean"),
        avg_humidity=("humidity", "mean"),
        avg_vibration=("vibration", "mean"),
        avg_environmental_risk=(
            "environmental_risk_score",
            "mean",
        ),
    ).reset_index()

    profile["anomaly_rate_pct"] = (
        profile["anomaly_records"]
        / profile["total_records"]
        * 100
    )

    profile["high_critical_rate_pct"] = (
        profile["high_critical_records"]
        / profile["total_records"]
        * 100
    )

    return profile


def create_daily_profile(df):
    """Analyze risk and anomalies by date."""

    grouped = df.groupby("date")

    profile = grouped.agg(
        total_records=("date", "size"),
        anomaly_records=(
            "predicted_condition",
            lambda x: (x.astype(str).str.upper() == "ANOMALY").sum(),
        ),
        high_critical_records=(
            "spoilage_risk",
            lambda x: x.astype(str).str.upper().isin(
                ["HIGH", "CRITICAL"]
            ).sum(),
        ),
        avg_environmental_risk=(
            "environmental_risk_score",
            "mean",
        ),
        avg_temperature=("temperature", "mean"),
        avg_humidity=("humidity", "mean"),
        avg_vibration=("vibration", "mean"),
    ).reset_index()

    profile["anomaly_rate_pct"] = (
        profile["anomaly_records"]
        / profile["total_records"]
        * 100
    )

    return profile


def create_priority_score(df):
    """
    Create an analytical operational priority score.

    This is a decision-support score for the simulated dataset.
    It is not a financial or causal risk model.
    """

    result = df.copy()

    result["priority_score"] = 0.0

    if "environmental_risk_score" in result.columns:
        result["priority_score"] += (
            result["environmental_risk_score"].fillna(0) * 10
        )

    if "predicted_condition" in result.columns:
        result.loc[
            result["predicted_condition"]
            .astype(str)
            .str.upper()
            .eq("WARNING"),
            "priority_score",
        ] += 15

        result.loc[
            result["predicted_condition"]
            .astype(str)
            .str.upper()
            .eq("ANOMALY"),
            "priority_score",
        ] += 30

    if "spoilage_risk" in result.columns:
        result.loc[
            result["spoilage_risk"]
            .astype(str)
            .str.upper()
            .eq("HIGH"),
            "priority_score",
        ] += 25

        result.loc[
            result["spoilage_risk"]
            .astype(str)
            .str.upper()
            .eq("CRITICAL"),
            "priority_score",
        ] += 50

    result["priority_level"] = pd.cut(
        result["priority_score"],
        bins=[-float("inf"), 30, 60, float("inf")],
        labels=["NORMAL", "HIGH", "CRITICAL"],
    )

    return result


def main():

    print("=" * 60)
    print("AtmoSync — Day 12 Advanced Analytics")
    print("=" * 60)

    telemetry, predictions, arbitrage = load_data()

    print(f"\nTelemetry records: {len(telemetry)}")
    print(f"Prediction records: {len(predictions)}")
    print(f"Arbitrage records: {len(arbitrage)}")

    df = prepare_data(
        telemetry,
        predictions,
        arbitrage,
    )

    print(f"Merged analytical records: {len(df)}")

    # Create profiles.
    container_profile = create_container_profile(df)
    commodity_profile = create_commodity_profile(df)
    hourly_profile = create_hourly_profile(df)
    daily_profile = create_daily_profile(df)

    # Priority analysis.
    priority_df = create_priority_score(df)

    # Print important summaries.
    print("\n--- Container Risk Profile ---")
    print(
        container_profile[
            [
                "container_id",
                "total_records",
                "anomaly_records",
                "anomaly_rate_pct",
                "avg_environmental_risk",
            ]
        ].to_string(index=False)
    )

    print("\n--- Commodity Risk Profile ---")
    print(
        commodity_profile[
            [
                "commodity",
                "total_records",
                "anomaly_records",
                "anomaly_rate_pct",
                "avg_environmental_risk",
            ]
        ].to_string(index=False)
    )

    print("\n--- Hourly Risk Profile ---")
    print(
        hourly_profile[
            [
                "hour",
                "total_records",
                "anomaly_records",
                "anomaly_rate_pct",
                "high_critical_rate_pct",
            ]
        ].to_string(index=False)
    )

    print("\n--- Priority Levels ---")
    print(
        priority_df["priority_level"]
        .value_counts(dropna=False)
        .sort_index()
    )

    # Save record-level advanced analytics.
    output_columns = [
        "container_id",
        "timestamp",
        "commodity",
        "temperature",
        "humidity",
        "vibration",
        "environmental_risk_score",
        "spoilage_risk",
        "predicted_condition",
        "prediction_confidence",
        "recommended_action",
        "arbitrage_opportunity",
        "hour",
        "day_of_week",
        "priority_score",
        "priority_level",
    ]

    available_output_columns = [
        column
        for column in output_columns
        if column in priority_df.columns
    ]

    priority_df[available_output_columns].to_csv(
        OUTPUT_FILE,
        index=False,
    )

    # Save separate analytical profiles.
    container_profile.to_csv(
        PROCESSED_DIR / "container_risk_profile.csv",
        index=False,
    )

    commodity_profile.to_csv(
        PROCESSED_DIR / "commodity_risk_profile.csv",
        index=False,
    )

    hourly_profile.to_csv(
        PROCESSED_DIR / "hourly_risk_profile.csv",
        index=False,
    )

    daily_profile.to_csv(
        PROCESSED_DIR / "daily_risk_profile.csv",
        index=False,
    )

    print("\nOutput files created:")
    print(f"- {OUTPUT_FILE.name}")
    print("- container_risk_profile.csv")
    print("- commodity_risk_profile.csv")
    print("- hourly_risk_profile.csv")
    print("- daily_risk_profile.csv")

    print("\nDay 12 advanced analytics completed successfully.")


if __name__ == "__main__":
    main()