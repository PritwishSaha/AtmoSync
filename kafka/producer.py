import csv
import json
import time
from kafka import KafkaProducer

KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "telemetry"
CSV_FILE = r"data\validated\validated_telemetry.csv"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

with open(CSV_FILE, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for count, row in enumerate(reader, start=1):

        message = {
            "container_id": row["container_id"],
            "timestamp": row["timestamp"],
            "commodity": row["commodity"],
            "temperature": float(row["temperature"]),
            "humidity": float(row["humidity"]),
            "vibration": float(row["vibration"]),
            "condition": row["condition"]
        }

        producer.send(TOPIC_NAME, value=message)

        print(f"Sent record {count}: {message}")

        time.sleep(0.1)

producer.flush()
producer.close()

print("\n1,785 records sent successfully.")