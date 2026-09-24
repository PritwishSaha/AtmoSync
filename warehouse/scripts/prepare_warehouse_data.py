"""
AtmoSync - Warehouse Data Preparation

Day 14:
Prepare validated telemetry data for the warehouse layer.

Source:
data/validated/validated_telemetry.csv

Output:
data/processed/warehouse_ready_telemetry.csv
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "validated" / "validated_telemetry.csv"
OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "warehouse_ready_telemetry.csv"
)

REQUIRED_COLUMNS = [
    "container_id",
    "timestamp",
    "commodity",
    "temperature",
    "humidity",
    "vibration",
    "condition",
]


def main():
    print("=" * 60)
    print("AtmoSync - Warehouse Data Preparation")
    print("=" * 60)

    print(f"\nReading source file:")
    print(INPUT_FILE)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Source file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(f"\nSource records: {len(df)}")
    print(f"Source columns: {list(df.columns)}")

    # Check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Keep only the warehouse table columns
    warehouse_df = df[REQUIRED_COLUMNS].copy()

    # Standardize timestamp
    warehouse_df["timestamp"] = pd.to_datetime(
        warehouse_df["timestamp"],
        errors="coerce"
    )

    if warehouse_df["timestamp"].isna().any():
        raise ValueError("Invalid timestamp values detected.")

    # Validate required fields
    if warehouse_df["container_id"].isna().any():
        raise ValueError("Missing container_id values detected.")

    if warehouse_df["commodity"].isna().any():
        raise ValueError("Missing commodity values detected.")

    if warehouse_df["condition"].isna().any():
        raise ValueError("Missing condition values detected.")

    # Validate sensor columns
    sensor_columns = [
        "temperature",
        "humidity",
        "vibration",
    ]

    for column in sensor_columns:
        warehouse_df[column] = pd.to_numeric(
            warehouse_df[column],
            errors="coerce"
        )

        if warehouse_df[column].isna().any():
            raise ValueError(
                f"Invalid numeric values detected in {column}."
            )

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save warehouse-ready dataset
    warehouse_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nWarehouse preparation completed.")
    print(f"Warehouse records: {len(warehouse_df)}")
    print(f"Warehouse columns: {list(warehouse_df.columns)}")
    print(f"Missing values: {warehouse_df.isna().sum().sum()}")
    print(f"Output file: {OUTPUT_FILE}")

    print("\nCondition distribution:")
    print(warehouse_df["condition"].value_counts())

    print("\nCommodity distribution:")
    print(warehouse_df["commodity"].value_counts())

    print("\n" + "=" * 60)
    print("WAREHOUSE DATA PREPARATION PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()