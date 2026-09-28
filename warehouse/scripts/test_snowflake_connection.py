import os
import snowflake.connector

conn = snowflake.connector.connect(
    account="TCBCWFI-XA77128",
    user="pritwishsaha",
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    role="ACCOUNTADMIN",
    database="ATMOSYNC_DB",
    warehouse="COMPUTE_WH",
    schema="TELEMETRY_SCHEMA",
)

cursor = conn.cursor()

try:
    cursor.execute("SELECT CURRENT_VERSION()")
    result = cursor.fetchone()

    print("Snowflake connection successful!")
    print("Snowflake version:", result[0])

finally:
    cursor.close()
    conn.close()