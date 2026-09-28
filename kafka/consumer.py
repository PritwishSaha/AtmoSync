import json
import os
from datetime import datetime

import snowflake.connector
from kafka import KafkaConsumer


# ==============================
# Kafka Configuration
# ==============================

KAFKA_SERVER = "localhost:9092"
TOPIC_NAME = "telemetry"

# ==============================
# Snowflake Configuration
# ==============================

SNOWFLAKE_ACCOUNT = "TCBCWFI-XA77128"
SNOWFLAKE_USER = "PRITWISHSAHA"
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")

SNOWFLAKE_DATABASE = "ATMOSYNC_DB"
SNOWFLAKE_SCHEMA = "TELEMETRY_SCHEMA"
SNOWFLAKE_TABLE = "RAW_TELEMETRY"


# ==============================
# Check Password
# ==============================

if not SNOWFLAKE_PASSWORD:
    raise RuntimeError(
        "SNOWFLAKE_PASSWORD environment variable is not set."
    )


# ==============================
# Connect to Snowflake
# ==============================

print("Connecting to Snowflake...")

conn = snowflake.connector.connect(
    account=SNOWFLAKE_ACCOUNT,
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
)

cursor = conn.cursor()

print("Snowflake connection successful!")


# ==============================
# Create Kafka Consumer
# ==============================

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id="atmosync-snowflake-loader",
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    ),
)

print("Kafka Consumer started.")
print(f"Listening to topic: {TOPIC_NAME}")
print("-" * 60)


# ==============================
# Statistics
# ==============================

processed = 0
inserted = 0
skipped = 0
failed = 0


try:

    for message in consumer:

        processed += 1

        data = message.value

        try:

            # ------------------------------
            # Extract Kafka message
            # ------------------------------

            container_id = data["container_id"]
            timestamp = datetime.fromisoformat(
                data["timestamp"]
            )

            commodity = data["commodity"]
            temperature = float(data["temperature"])
            humidity = float(data["humidity"])
            vibration = float(data["vibration"])
            condition = data["condition"]


            # ------------------------------
            # Duplicate Check
            # ------------------------------

            check_sql = f"""
                SELECT COUNT(*)
                FROM {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{SNOWFLAKE_TABLE}
                WHERE CONTAINER_ID = %s
                  AND TIMESTAMP = %s
            """

            cursor.execute(
                check_sql,
                (container_id, timestamp)
            )

            existing = cursor.fetchone()[0]


            # ------------------------------
            # Skip Duplicate
            # ------------------------------

            if existing > 0:

                skipped += 1

                print(
                    f"[SKIP] {container_id} | "
                    f"{timestamp} | already exists"
                )

            # ------------------------------
            # Insert New Record
            # ------------------------------

            else:

                insert_sql = f"""
                    INSERT INTO
                    {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{SNOWFLAKE_TABLE}
                    (
                        CONTAINER_ID,
                        TIMESTAMP,
                        COMMODITY,
                        TEMPERATURE,
                        HUMIDITY,
                        VIBRATION,
                        CONDITION
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(
                    insert_sql,
                    (
                        container_id,
                        timestamp,
                        commodity,
                        temperature,
                        humidity,
                        vibration,
                        condition
                    )
                )

                conn.commit()

                inserted += 1

                print(
                    f"[INSERT] {container_id} | "
                    f"{timestamp} | {commodity}"
                )


        except Exception as e:

            failed += 1

            print(
                f"[ERROR] Message {processed}: {e}"
            )


        # ------------------------------
        # Commit Kafka offset
        # ------------------------------

        consumer.commit()


        # ------------------------------
        # Stop after all expected records
        # ------------------------------

        if processed == 1785:
            break


finally:

    consumer.close()
    cursor.close()
    conn.close()


# ==============================
# Final Summary
# ==============================

print("\n" + "=" * 60)
print("AtmoSync Kafka → Snowflake ingestion completed")
print("=" * 60)

print(f"Messages processed : {processed}")
print(f"Records inserted   : {inserted}")
print(f"Records skipped    : {skipped}")
print(f"Records failed     : {failed}")