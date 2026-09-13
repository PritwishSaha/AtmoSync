import pandas as pd
from pathlib import Path


# ============================================================
# AtmoSync - Day 6
# Micro-Climate Risk Analytics
# ============================================================

INPUT_FILE = Path("data/processed/iot_telemetry_features.csv")

HIGH_RISK_FILE = Path(
    "data/processed/high_risk_telemetry.csv"
)

CONTAINER_FILE = Path(
    "data/processed/container_risk_summary.csv"
)

COMMODITY_FILE = Path(
    "data/processed/commodity_risk_summary.csv"
)


def load_data():
    """Load Day 5 feature-engineered dataset."""

    print("\n[1] Loading processed telemetry...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Rows loaded: {len(df)}")
    print(f"Columns loaded: {len(df.columns)}")

    return df


def overall_risk_analysis(df):
    """Analyze overall environmental and spoilage risk."""

    print("\n[2] Overall risk analysis")

    print("\nCondition distribution:")
    print(df["condition"].value_counts())

    print("\nSpoilage risk distribution:")
    print(df["spoilage_risk"].value_counts())

    print("\nEnvironmental risk distribution:")
    print(df["environmental_risk"].value_counts())

    print("\nAverage environmental risk:")
    print(
        round(
            df["environmental_risk_score"].mean(),
            3
        )
    )


def create_risk_percentages(df):
    """Calculate spoilage risk percentages."""

    print("\n[3] Calculating risk percentages...")

    risk_summary = (
        df["spoilage_risk"]
        .value_counts()
        .rename_axis("spoilage_risk")
        .reset_index(name="record_count")
    )

    total = len(df)

    risk_summary["percentage"] = (
        risk_summary["record_count"] / total * 100
    ).round(2)

    print(risk_summary)

    return risk_summary


def create_container_summary(df):
    """Create container-level risk summary."""

    print("\n[4] Creating container risk summary...")

    summary = (
        df.groupby("container_id")
        .agg(
            total_records=("container_id", "size"),

            warning_count=(
                "condition",
                lambda x: (x == "WARNING").sum()
            ),

            anomaly_count=(
                "condition",
                lambda x: (x == "ANOMALY").sum()
            ),

            high_risk_count=(
                "spoilage_risk",
                lambda x: (x == "HIGH").sum()
            ),

            critical_count=(
                "spoilage_risk",
                lambda x: (x == "CRITICAL").sum()
            ),

            avg_temperature=(
                "temperature",
                "mean"
            ),

            avg_humidity=(
                "humidity",
                "mean"
            ),

            avg_vibration=(
                "vibration",
                "mean"
            ),

            avg_environmental_risk=(
                "environmental_risk_score",
                "mean"
            ),

            max_environmental_risk=(
                "environmental_risk_score",
                "max"
            )
        )
        .reset_index()
    )

    summary["avg_environmental_risk"] = (
        summary["avg_environmental_risk"]
        .round(3)
    )

    summary["avg_temperature"] = (
        summary["avg_temperature"]
        .round(2)
    )

    summary["avg_humidity"] = (
        summary["avg_humidity"]
        .round(2)
    )

    summary["avg_vibration"] = (
        summary["avg_vibration"]
        .round(3)
    )

    summary["risk_status"] = "LOW"

    summary.loc[
        summary["avg_environmental_risk"] >= 2,
        "risk_status"
    ] = "MEDIUM"

    summary.loc[
        summary["avg_environmental_risk"] >= 3,
        "risk_status"
    ] = "HIGH"

    summary.loc[
        summary["critical_count"] > 0,
        "risk_status"
    ] = "CRITICAL"

    summary = summary.sort_values(
        "avg_environmental_risk",
        ascending=False
    )

    summary.to_csv(
        CONTAINER_FILE,
        index=False
    )

    print("\nContainer risk ranking:")
    print(summary.to_string(index=False))

    print(
        f"\nSaved: {CONTAINER_FILE}"
    )

    return summary


def create_commodity_summary(df):
    """Create commodity-level risk summary."""

    print("\n[5] Creating commodity risk summary...")

    summary = (
        df.groupby("commodity")
        .agg(
            total_records=("commodity", "size"),

            warning_count=(
                "condition",
                lambda x: (x == "WARNING").sum()
            ),

            anomaly_count=(
                "condition",
                lambda x: (x == "ANOMALY").sum()
            ),

            high_risk_count=(
                "spoilage_risk",
                lambda x: (x == "HIGH").sum()
            ),

            critical_count=(
                "spoilage_risk",
                lambda x: (x == "CRITICAL").sum()
            ),

            avg_temperature=(
                "temperature",
                "mean"
            ),

            avg_humidity=(
                "humidity",
                "mean"
            ),

            avg_vibration=(
                "vibration",
                "mean"
            ),

            avg_environmental_risk=(
                "environmental_risk_score",
                "mean"
            )
        )
        .reset_index()
    )

    summary["avg_environmental_risk"] = (
        summary["avg_environmental_risk"]
        .round(3)
    )

    summary["avg_temperature"] = (
        summary["avg_temperature"]
        .round(2)
    )

    summary["avg_humidity"] = (
        summary["avg_humidity"]
        .round(2)
    )

    summary["avg_vibration"] = (
        summary["avg_vibration"]
        .round(3)
    )

    summary["risk_status"] = "LOW"

    summary.loc[
        summary["avg_environmental_risk"] >= 2,
        "risk_status"
    ] = "MEDIUM"

    summary.loc[
        summary["avg_environmental_risk"] >= 3,
        "risk_status"
    ] = "HIGH"

    summary.loc[
        summary["critical_count"] > 0,
        "risk_status"
    ] = "CRITICAL"

    summary = summary.sort_values(
        "avg_environmental_risk",
        ascending=False
    )

    summary.to_csv(
        COMMODITY_FILE,
        index=False
    )

    print("\nCommodity risk ranking:")
    print(summary.to_string(index=False))

    print(
        f"\nSaved: {COMMODITY_FILE}"
    )

    return summary


def create_high_risk_dataset(df):
    """Extract HIGH and CRITICAL spoilage-risk records."""

    print("\n[6] Creating high-risk telemetry dataset...")

    high_risk = df[
        df["spoilage_risk"].isin(
            ["HIGH", "CRITICAL"]
        )
    ].copy()

    high_risk = high_risk.sort_values(
        "environmental_risk_score",
        ascending=False
    )

    high_risk.to_csv(
        HIGH_RISK_FILE,
        index=False
    )

    print(
        f"High-risk records: {len(high_risk)}"
    )

    print(
        f"Saved: {HIGH_RISK_FILE}"
    )

    return high_risk


def environmental_analysis(df):
    """Analyze environmental conditions associated with risk."""

    print("\n[7] Environmental condition analysis")

    high_risk = df[
        df["spoilage_risk"].isin(
            ["HIGH", "CRITICAL"]
        )
    ]

    print("\nOverall sensor averages:")

    print(
        df[
            [
                "temperature",
                "humidity",
                "vibration"
            ]
        ].mean().round(3)
    )

    print("\nHIGH/CRITICAL sensor averages:")

    print(
        high_risk[
            [
                "temperature",
                "humidity",
                "vibration"
            ]
        ].mean().round(3)
    )


def print_key_findings(df, container_summary, commodity_summary):
    """Print important business findings."""

    print("\n[8] Key findings")

    highest_container = container_summary.iloc[0]

    highest_commodity = commodity_summary.iloc[0]

    high_critical_count = len(
        df[
            df["spoilage_risk"].isin(
                ["HIGH", "CRITICAL"]
            )
        ]
    )

    print(
        f"\nHighest-risk container: "
        f"{highest_container['container_id']}"
    )

    print(
        f"Container average risk: "
        f"{highest_container['avg_environmental_risk']}"
    )

    print(
        f"\nHighest-risk commodity: "
        f"{highest_commodity['commodity']}"
    )

    print(
        f"Commodity average risk: "
        f"{highest_commodity['avg_environmental_risk']}"
    )

    print(
        f"\nHIGH/CRITICAL records: "
        f"{high_critical_count}"
    )


def main():

    print("=" * 60)
    print("AtmoSync - Day 6 Micro-Climate Risk Analytics")
    print("=" * 60)

    df = load_data()

    overall_risk_analysis(df)

    risk_summary = create_risk_percentages(df)

    container_summary = create_container_summary(df)

    commodity_summary = create_commodity_summary(df)

    high_risk = create_high_risk_dataset(df)

    environmental_analysis(df)

    print_key_findings(
        df,
        container_summary,
        commodity_summary
    )

    print("\n" + "=" * 60)
    print("DAY 6 ANALYTICS COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()