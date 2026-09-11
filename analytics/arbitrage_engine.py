import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# AtmoSync - Arbitrage Analytics Engine
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "iot_telemetry_spoilage.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "atmosync_arbitrage.csv"
)

print("=" * 60)
print("ATMOSYNC - ARBITRAGE ANALYTICS ENGINE")
print("=" * 60)

# ---------------------------------------------------------
# Load spoilage data
# ---------------------------------------------------------

print("\nLoading spoilage telemetry...")

df = pd.read_csv(INPUT_FILE)

print(f"Rows loaded: {len(df)}")

# ---------------------------------------------------------
# Analytical commodity market assumptions
# ---------------------------------------------------------
# These are project assumptions for demonstrating the
# arbitrage analytics concept.
#
# They are NOT live market prices.

COMMODITY_MARKET = {
    "Avocado": {
        "market_price": 180,
        "spoilage_value_factor": 0.45
    },
    "Banana": {
        "market_price": 70,
        "spoilage_value_factor": 0.35
    },
    "Mango": {
        "market_price": 140,
        "spoilage_value_factor": 0.40
    },
    "Tomato": {
        "market_price": 60,
        "spoilage_value_factor": 0.30
    }
}

# ---------------------------------------------------------
# Map commodity assumptions
# ---------------------------------------------------------

df["market_price_per_kg"] = df["commodity"].map(
    lambda x: COMMODITY_MARKET[x]["market_price"]
)

df["spoilage_value_factor"] = df["commodity"].map(
    lambda x: COMMODITY_MARKET[x]["spoilage_value_factor"]
)

# ---------------------------------------------------------
# Estimate affected value
# ---------------------------------------------------------
# Assume each telemetry observation represents 100 kg
# of monitored commodity for this project model.

ASSUMED_CARGO_KG = 100

df["cargo_value"] = (
    df["market_price_per_kg"]
    * ASSUMED_CARGO_KG
)

# ---------------------------------------------------------
# Potential spoilage loss
# ---------------------------------------------------------

df["potential_spoilage_loss"] = (
    df["cargo_value"]
    * df["spoilage_value_factor"]
    * (df["spoilage_risk_score"] / 100)
)

df["potential_spoilage_loss"] = (
    df["potential_spoilage_loss"]
    .round(2)
)

# ---------------------------------------------------------
# Opportunity score
# ---------------------------------------------------------
# Higher spoilage risk + higher commodity value =
# higher intervention priority.

df["opportunity_score"] = (
    df["spoilage_risk_score"]
    * df["market_price_per_kg"]
) / 100

df["opportunity_score"] = (
    df["opportunity_score"]
    .round(2)
)

# ---------------------------------------------------------
# Action recommendation
# ---------------------------------------------------------

def recommend_action(row):

    score = row["spoilage_risk_score"]

    if score >= 80:
        return "URGENT_REROUTE"

    elif score >= 60:
        return "PRIORITIZE_DELIVERY"

    elif score >= 40:
        return "MONITOR_CLOSELY"

    else:
        return "NORMAL_TRANSIT"


df["recommended_action"] = df.apply(
    recommend_action,
    axis=1
)

# ---------------------------------------------------------
# Arbitrage opportunity flag
# ---------------------------------------------------------

df["arbitrage_opportunity"] = (
    (df["spoilage_risk_score"] >= 60)
    & (df["market_price_per_kg"] >= 100)
)

# ---------------------------------------------------------
# Save result
# ---------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

print("\nArbitrage analytics completed.")

print(f"\nFinal rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")

print("\nRecommended Actions:")
print(
    df["recommended_action"]
    .value_counts()
)

print("\nPotential Spoilage Loss by Commodity:")

print(
    df.groupby("commodity")[
        "potential_spoilage_loss"
    ]
    .sum()
    .sort_values(ascending=False)
    .round(2)
)

print("\nAverage Opportunity Score by Commodity:")

print(
    df.groupby("commodity")[
        "opportunity_score"
    ]
    .mean()
    .sort_values(ascending=False)
    .round(2)
)

print("\nArbitrage Opportunities:")

print(
    df["arbitrage_opportunity"]
    .value_counts()
)

print("\nTop 10 Arbitrage Opportunities:")

columns = [
    "container_id",
    "commodity",
    "market_price_per_kg",
    "spoilage_risk_score",
    "spoilage_risk",
    "potential_spoilage_loss",
    "opportunity_score",
    "recommended_action",
    "arbitrage_opportunity"
]

print(
    df[
        df["arbitrage_opportunity"]
    ]
    .nlargest(
        10,
        "opportunity_score"
    )[columns]
    .to_string(index=False)
)

print("\nOutput:")
print(OUTPUT_FILE)

print("\n" + "=" * 60)
print("ARBITRAGE ANALYTICS COMPLETED")
print("=" * 60)