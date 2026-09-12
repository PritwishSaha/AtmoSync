import random
import time
import csv
import os
from datetime import datetime


# ============================================================
# ATMOSYNC - IoT TELEMETRY SIMULATOR
# ============================================================

CONTAINERS = [
    "CONT_001",
    "CONT_002",
    "CONT_003",
    "CONT_004",
    "CONT_005"
]


# Initial analytical operating ranges.
# These are project assumptions and should be validated against
# authoritative commodity-specific storage guidance.

COMMODITY_RANGES = {

    "Avocado": {
        "temperature": (5, 13),
        "humidity": (85, 95)
    },

    "Banana": {
        "temperature": (13, 14),
        "humidity": (85, 95)
    },

    "Mango": {
        "temperature": (10, 13),
        "humidity": (85, 90)
    },

    "Tomato": {
        "temperature": (10, 12),
        "humidity": (85, 95)
    }
}


COMMODITIES = list(COMMODITY_RANGES.keys())


def generate_sensor_data():

    # Select container
    container_id = random.choice(CONTAINERS)

    # Select commodity
    commodity = random.choice(COMMODITIES)

    # Get commodity-specific operating range
    rules = COMMODITY_RANGES[commodity]

    temp_min, temp_max = rules["temperature"]
    humidity_min, humidity_max = rules["humidity"]

    # --------------------------------------------------------
    # Select operating condition
    # --------------------------------------------------------

    condition = random.choices(
        ["NORMAL", "WARNING", "ANOMALY"],
        weights=[70, 20, 10],
        k=1
    )[0]


    # --------------------------------------------------------
    # Generate telemetry based on condition
    # --------------------------------------------------------

    if condition == "NORMAL":

        temperature = round(
            random.uniform(temp_min, temp_max),
            2
        )

        humidity = round(
            random.uniform(humidity_min, humidity_max),
            2
        )

        vibration = round(
            random.uniform(0.05, 0.20),
            2
        )


    elif condition == "WARNING":

        # Moderate temperature deviation
        temperature = round(
            random.choice([
                random.uniform(temp_min - 3, temp_min - 1),
                random.uniform(temp_max + 1, temp_max + 3)
            ]),
            2
        )

        # Moderate humidity deviation
        humidity = round(
            random.choice([
                random.uniform(max(0, humidity_min - 25), max(0, humidity_min - 10)),
                random.uniform(min(100, humidity_max + 10), 100)
    ]),
    2
)

        vibration = round(
            random.uniform(0.20, 0.35),
            2
        )


    else:

        # Strong temperature deviation
        temperature = round(
            random.choice([
                random.uniform(temp_min - 7, temp_min - 3),
                random.uniform(temp_max + 3, temp_max + 7)
            ]),
            2
        )

        # Strong humidity deviation
        humidity = round(
            random.choice([
                random.uniform(humidity_min - 25, humidity_min - 10),
                random.uniform(humidity_max + 10, humidity_max + 20)
            ]),
            2
        )

        # High vibration
        vibration = round(
            random.uniform(0.35, 0.60),
            2
        )

    temperature = round(temperature, 2)
    humidity = round(max(0, min(100, humidity)), 2)
    vibration = round(max(0, vibration), 2)
    timestamp = datetime.now().isoformat()


    return {
        "container_id": container_id,
        "timestamp": timestamp,
        "commodity": commodity,
        "temperature": temperature,
        "humidity": humidity,
        "vibration": vibration,
        "condition": condition
    }


def save_to_csv(sensor_data):

    file_path = "data/raw/iot_telemetry.csv"

    os.makedirs("data/raw", exist_ok=True)

    file_exists = os.path.isfile(file_path)


    with open(
        file_path,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "container_id",
            "timestamp",
            "commodity",
            "temperature",
            "humidity",
            "vibration",
            "condition"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )


        if not file_exists:
            writer.writeheader()


        writer.writerow(sensor_data)


def main():

    print("AtmoSync IoT Simulator Started")
    print("-" * 70)

    try:

        while True:

            sensor_data = generate_sensor_data()

            save_to_csv(sensor_data)


            print(
                f"Container: {sensor_data['container_id']} | "
                f"Commodity: {sensor_data['commodity']} | "
                f"Temperature: {sensor_data['temperature']}°C | "
                f"Humidity: {sensor_data['humidity']}% | "
                f"Vibration: {sensor_data['vibration']} | "
                f"Condition: {sensor_data['condition']}"
            )


            time.sleep(2)


    except KeyboardInterrupt:

        print("\nIoT Simulator stopped.")


if __name__ == "__main__":
    main()