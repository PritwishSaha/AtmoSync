import pandas as pd
from pathlib import Path


RAW_FILE = Path("data/raw/iot_telemetry.csv")
VALIDATED_FILE = Path("data/validated/validated_telemetry.csv")


def validate_data():

    print("=" * 60)
    print("AtmoSync - IoT Telemetry Data Validation")
    print("=" * 60)

    # Load dataset
    df = pd.read_csv(RAW_FILE)

    print(f"\nTotal records: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    # --------------------------------------------------
    # 1. Required Columns
    # --------------------------------------------------

    required_columns = [
        "container_id",
        "timestamp",
        "commodity",
        "temperature",
        "humidity",
        "vibration",
        "condition"
    ]

    print("\n[1] Checking required columns...")

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        print("FAIL - Missing columns:", missing_columns)
        return

    print("PASS - All required columns exist.")

    # --------------------------------------------------
    # 2. Missing Values
    # --------------------------------------------------

    print("\n[2] Missing value analysis")

    missing_values = df.isnull().sum()

    print(missing_values)

    total_missing = missing_values.sum()

    if total_missing == 0:
        print("PASS - No missing values found.")
    else:
        print(f"WARNING - {total_missing} missing values found.")

    # --------------------------------------------------
    # 3. Duplicate Records
    # --------------------------------------------------

    print("\n[3] Duplicate analysis")

    duplicates = df.duplicated().sum()

    print(f"Duplicate rows: {duplicates}")

    if duplicates == 0:
        print("PASS - No duplicate rows found.")
    else:
        print("WARNING - Duplicate rows detected.")

    # --------------------------------------------------
    # 4. Data Types
    # --------------------------------------------------

    print("\n[4] Data type validation")

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    print(df.dtypes)

    invalid_timestamps = df["timestamp"].isna().sum()

    if invalid_timestamps == 0:
        print("PASS - All timestamps are valid.")
    else:
        print(
            f"WARNING - {invalid_timestamps} invalid timestamps found."
        )

    # --------------------------------------------------
    # 5. Sensor Range Validation
    # --------------------------------------------------

    print("\n[5] Sensor range validation")

    invalid_temperature = (
        (df["temperature"] < -20) |
        (df["temperature"] > 60)
    ).sum()

    invalid_humidity = (
        (df["humidity"] < 0) |
        (df["humidity"] > 100)
    ).sum()

    invalid_vibration = (
        df["vibration"] < 0
    ).sum()

    print(f"Invalid temperature values: {invalid_temperature}")
    print(f"Invalid humidity values: {invalid_humidity}")
    print(f"Invalid vibration values: {invalid_vibration}")

    if (
        invalid_temperature == 0
        and invalid_humidity == 0
        and invalid_vibration == 0
    ):
        print("PASS - Sensor values are within valid ranges.")
    else:
        print("WARNING - Invalid sensor values detected.")

    # --------------------------------------------------
    # 6. Condition Validation
    # --------------------------------------------------

    print("\n[6] Condition validation")

    valid_conditions = [
    "NORMAL",
    "WARNING",
    "ANOMALY"
]

    invalid_conditions = (
        ~df["condition"].isin(valid_conditions)
    ).sum()

    print(f"Invalid condition values: {invalid_conditions}")

    if invalid_conditions == 0:
        print("PASS - All condition values are valid.")
    else:
        print("WARNING - Invalid condition values found.")

    # --------------------------------------------------
    # 7. Commodity Analysis
    # --------------------------------------------------

    print("\n[7] Commodity distribution")

    print(df["commodity"].value_counts())

    # --------------------------------------------------
    # 8. Container Analysis
    # --------------------------------------------------

    print("\n[8] Container distribution")

    print(df["container_id"].value_counts())

    # --------------------------------------------------
    # 9. Sensor Statistics
    # --------------------------------------------------

    print("\n[9] Sensor statistics")

    sensor_columns = [
        "temperature",
        "humidity",
        "vibration"
    ]

    print(df[sensor_columns].describe())

    # --------------------------------------------------
    # 10. Save Validated Dataset
    # --------------------------------------------------

    VALIDATED_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        VALIDATED_FILE,
        index=False
    )

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print(f"\nValidated dataset saved to:")
    print(VALIDATED_FILE)


if __name__ == "__main__":
    validate_data()