"""
AtmoSync IoT Telemetry Simulator

Generates simulated container telemetry including:
- Temperature
- Humidity
- Vibration
- Timestamp
- Container ID
"""
import random
import time
from datetime import datetime


CONTAINERS = ["CONT_001", "CONT_002", "CONT_003", "CONT_004", "CONT_005"]


def generate_sensor_data():
    container_id = random.choice(CONTAINERS)

    temperature = round(random.uniform(5, 10), 2)
    humidity = round(random.uniform(60, 80), 2)
    vibration = round(random.uniform(0.1, 0.4), 2)

    timestamp = datetime.now().isoformat()

    return {
        "container_id": container_id,
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity,
        "vibration": vibration
    }


def main():
    print("AtmoSync IoT Simulator Started")
    print("-" * 50)

    while True:
        sensor_data = generate_sensor_data()

        print(
            f"Container: {sensor_data['container_id']} | "
            f"Time: {sensor_data['timestamp']} | "
            f"Temperature: {sensor_data['temperature']}°C | "
            f"Humidity: {sensor_data['humidity']}% | "
            f"Vibration: {sensor_data['vibration']}"
    )

        time.sleep(2)


if __name__ == "__main__":
    main()