import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


# ============================================================
# AtmoSync - Snowflake Data Loader
# ============================================================

CSV_FILE = "data/processed/warehouse_ready_telemetry.csv"

DATABASE = "ATMOSYNC_DB"
SCHEMA = "TELEMETRY_SCHEMA"
TABLE = "RAW_TELEMETRY"


print("=" * 60)
print("AtmoSync - Snowflake Data Loader")
print("=" * 60)


# ------------------------------------------------------------
# 1. Read prepared CSV
# ------------------------------------------------------------

print("\nReading warehouse data...")

df = pd.read_csv(CSV_FILE)

print(f"Records loaded from CSV: {len(df)}")
print(f"Columns: {list(df.columns)}")


# Convert timestamp column to datetime
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="%Y-%m-%d %H:%M:%S.%f"
).dt.strftime("%Y-%m-%d %H:%M:%S.%f")


# ------------------------------------------------------------
# 2. Read Snowflake credentials from environment variables
# ------------------------------------------------------------

user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
account = os.getenv("SNOWFLAKE_ACCOUNT")


if not user:
    raise ValueError("SNOWFLAKE_USER environment variable is missing.")

if not password:
    raise ValueError("SNOWFLAKE_PASSWORD environment variable is missing.")

if not account:
    raise ValueError("SNOWFLAKE_ACCOUNT environment variable is missing.")


# ------------------------------------------------------------
# 3. Connect to Snowflake
# ------------------------------------------------------------

print("\nConnecting to Snowflake...")

conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    database=DATABASE,
    schema=SCHEMA,
)

print("Snowflake connection: SUCCESS")


# ------------------------------------------------------------
# 4. Upload DataFrame to Snowflake
# ------------------------------------------------------------

print("\nUploading data to Snowflake...")

success, nchunks, nrows, output = write_pandas(
    conn=conn,
    df=df,
    table_name=TABLE,
    database=DATABASE,
    schema=SCHEMA,
    auto_create_table=False,
    overwrite=False,
    quote_identifiers=False,
)

print(f"Upload success: {success}")
print(f"Chunks uploaded: {nchunks}")
print(f"Rows uploaded: {nrows}")


# ------------------------------------------------------------
# 5. Verify row count in Snowflake
# ------------------------------------------------------------

cursor = conn.cursor()

cursor.execute(
    f"""
    SELECT COUNT(*)
    FROM {DATABASE}.{SCHEMA}.{TABLE}
    """
)

count = cursor.fetchone()[0]

print("\nSnowflake row count:", count)


# ------------------------------------------------------------
# 6. Close connection
# ------------------------------------------------------------

cursor.close()
conn.close()


print("\n" + "=" * 60)
print("SNOWFLAKE LOAD COMPLETED")
print("=" * 60)