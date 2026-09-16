import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "iot_telemetry_features.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_FILE = MODEL_DIR / "condition_prediction_model.pkl"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "ml_predictions.csv"


# --------------------------------------------------
# 2. Create model directory
# --------------------------------------------------

MODEL_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# 3. Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset shape:", df.shape)


# --------------------------------------------------
# 4. Define target
# --------------------------------------------------

target = "condition"


# --------------------------------------------------
# 5. Select ML features
# --------------------------------------------------

features = [
    "temperature",
    "humidity",
    "vibration",
    "hour",
    "day_of_week",
    "commodity",
    "container_id"
]

X = df[features]
y = df[target]


# --------------------------------------------------
# 6. Identify categorical and numerical columns
# --------------------------------------------------

categorical_features = [
    "commodity",
    "container_id"
]

numerical_features = [
    "temperature",
    "humidity",
    "vibration",
    "hour",
    "day_of_week"
]


# --------------------------------------------------
# 7. Preprocessing
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# --------------------------------------------------
# 8. Create Random Forest model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# --------------------------------------------------
# 9. Create pipeline
# --------------------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# --------------------------------------------------
# 10. Train-test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("Training records:", len(X_train))
print("Testing records:", len(X_test))


# --------------------------------------------------
# 11. Train model
# --------------------------------------------------

print("\nTraining Random Forest model...")

pipeline.fit(X_train, y_train)


# --------------------------------------------------
# 12. Predictions
# --------------------------------------------------

y_pred = pipeline.predict(X_test)


# --------------------------------------------------
# 13. Evaluation
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print(round(accuracy, 4))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# --------------------------------------------------
# 14. Save model
# --------------------------------------------------

joblib.dump(pipeline, MODEL_FILE)

print("\nModel saved to:")
print(MODEL_FILE)


# --------------------------------------------------
# 15. Generate predictions for complete dataset
# --------------------------------------------------

df["predicted_condition"] = pipeline.predict(X)

df["prediction_confidence"] = pipeline.predict_proba(X).max(axis=1)

df["prediction_correct"] = (
    df["condition"] == df["predicted_condition"]
)


# --------------------------------------------------
# 16. Save predictions
# --------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\nPrediction file saved to:")
print(OUTPUT_FILE)

print("\nPrediction distribution:")
print(df["predicted_condition"].value_counts())

print("\nAverage prediction confidence:")
print(round(df["prediction_confidence"].mean(), 4))

print("\nDay 8 ML training completed successfully.")