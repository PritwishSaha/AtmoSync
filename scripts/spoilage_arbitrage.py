import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# 1. File paths
# ---------------------------------------------------------

INPUT_FILE = Path("data/processed/iot_telemetry_features.csv")
OUTPUT_FILE = Path("data/processed/arbitrage_decisions.csv")


# ---------------------------------------------------------
# 2. Load processed telemetry
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Input dataset shape:", df.shape)


# ---------------------------------------------------------
# 3. Create business action
# ---------------------------------------------------------

def recommend_action(risk):
    if risk == "CRITICAL":
        return "URGENT INTERVENTION"
    elif risk == "HIGH":
        return "CONSIDER REROUTING"
    elif risk == "MEDIUM":
        return "INCREASE MONITORING"
    else:
        return "CONTINUE MONITORING"


df["recommended_action"] = df["spoilage_risk"].apply(
    recommend_action
)


# ---------------------------------------------------------
# 4. Create priority
# ---------------------------------------------------------

def assign_priority(risk):
    if risk == "CRITICAL":
        return "P1"
    elif risk == "HIGH":
        return "P2"
    elif risk == "MEDIUM":
        return "P3"
    else:
        return "P4"


df["priority"] = df["spoilage_risk"].apply(
    assign_priority
)


# ---------------------------------------------------------
# 5. Create intervention flag
# ---------------------------------------------------------

df["intervention_required"] = df["spoilage_risk"].isin(
    ["HIGH", "CRITICAL"]
)


# ---------------------------------------------------------
# 6. Create arbitrage opportunity flag
# ---------------------------------------------------------

df["arbitrage_opportunity"] = (
    df["spoilage_risk"].isin(["HIGH", "CRITICAL"])
    & (df["environmental_risk_score"] >= 6)
)


# ---------------------------------------------------------
# 7. Create business reason
# ---------------------------------------------------------

def generate_reason(row):

    reasons = []

    if row["temperature"] > 15:
        reasons.append("high temperature")

    if row["humidity"] >= 95:
        reasons.append("high humidity")

    if row["vibration"] >= 0.35:
        reasons.append("elevated vibration")

    if row["condition"] == "ANOMALY":
        reasons.append("sensor anomaly")

    if not reasons:
        reasons.append("elevated environmental risk")

    return ", ".join(reasons)


df["decision_reason"] = df.apply(
    generate_reason,
    axis=1
)


# ---------------------------------------------------------
# 8. Create decision score
# ---------------------------------------------------------

def calculate_decision_score(row):

    score = row["environmental_risk_score"]

    if row["temperature"] > 15:
        score += 1

    if row["humidity"] >= 95:
        score += 1

    if row["vibration"] >= 0.35:
        score += 1

    if row["condition"] == "ANOMALY":
        score += 1

    return score


df["decision_score"] = df.apply(
    calculate_decision_score,
    axis=1
)


# ---------------------------------------------------------
# 9. Export decision dataset
# ---------------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# ---------------------------------------------------------
# 10. Summary
# ---------------------------------------------------------

print("\nDecision dataset created successfully.")
print("Output:", OUTPUT_FILE)
print("Shape:", df.shape)

print("\nRecommended Actions:")
print(df["recommended_action"].value_counts())

print("\nPriority Distribution:")
print(df["priority"].value_counts())

print("\nIntervention Required:")
print(df["intervention_required"].value_counts())

print("\nArbitrage Opportunities:")
print(df["arbitrage_opportunity"].value_counts())

print("\nTop Decision Records:")
print(
    df[
        [
            "container_id",
            "commodity",
            "spoilage_risk",
            "environmental_risk_score",
            "recommended_action",
            "priority",
            "arbitrage_opportunity",
            "decision_reason"
        ]
    ]
    .sort_values("decision_score", ascending=False)
    .head(10)
)