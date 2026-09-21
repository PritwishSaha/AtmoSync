from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "iot_telemetry.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "pipeline_sample.csv"


def run_pipeline():

    print("=" * 60)
    print("AtmoSync — Day 13 Local Pipeline Prototype")
    print("=" * 60)

    print("\n[1] Reading raw telemetry...")

    df = pd.read_csv(RAW_FILE)

    print(f"Raw records: {len(df)}")

    print("\n[2] Validating required columns...")

    required_columns = [
        "container_id",
        "timestamp",
        "commodity",
        "temperature",
        "humidity",
        "vibration",
        "condition"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    print("Schema validation: PASSED")

    print("\n[3] Checking missing values...")

    missing_values = (
        df[required_columns]
        .isna()
        .sum()
        .sum()
    )

    print(f"Missing values: {missing_values}")

    if missing_values > 0:
        raise ValueError("Missing values detected.")

    print("Data quality check: PASSED")

    print("\n[4] Selecting pipeline fields...")

    pipeline_df = df[required_columns].copy()

    print(f"Pipeline records: {len(pipeline_df)}")

    print("\n[5] Writing pipeline output...")

    pipeline_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Output: {OUTPUT_FILE}")

    print("\n[6] Pipeline summary")

    print(f"Records processed: {len(pipeline_df)}")
    print(
        "Commodities:",
        pipeline_df["commodity"].nunique()
    )
    print(
        "Containers:",
        pipeline_df["container_id"].nunique()
    )

    print("\nDay 13 local pipeline prototype completed.")


if __name__ == "__main__":
    run_pipeline()