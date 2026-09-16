# Day 8 — Micro-Climate Condition Prediction

## 1. Objective

The objective of Day 8 was to introduce a machine learning
classification layer into the AtmoSync analytics pipeline.

The model predicts telemetry conditions as NORMAL, WARNING,
or ANOMALY.

## 2. Dataset

The model was trained using the processed AtmoSync IoT
telemetry dataset containing 1,785 records.

## 3. Target Variable

The target variable is `condition`.

Classes:

- NORMAL
- WARNING
- ANOMALY

## 4. Input Features

The model uses:

- temperature
- humidity
- vibration
- hour
- day_of_week
- commodity
- container_id

Risk and business decision fields were excluded to reduce
target leakage.

## 5. Preprocessing

Categorical variables were converted using OneHotEncoder.

Numerical variables were passed directly to the model.

A Scikit-learn Pipeline was used to combine preprocessing
and model training.

## 6. Train-Test Split

The dataset was divided into:

- 80% training data
- 20% testing data

Stratified splitting was used to preserve class distribution.

## 7. Machine Learning Model

Random Forest Classifier was used.

Configuration:

- n_estimators = 200
- random_state = 42
- class_weight = balanced

## 8. Model Evaluation

Accuracy:

[PUT YOUR ACTUAL ACCURACY HERE]

Precision, recall and F1-score:

[PUT YOUR ACTUAL CLASSIFICATION REPORT VALUES HERE]

## 9. Confusion Matrix

The confusion matrix was used to identify correct predictions
and misclassifications between NORMAL, WARNING and ANOMALY.

## 10. Feature Importance

Random Forest feature importance was analyzed to understand
which telemetry and contextual variables contributed most to
the model.

## 11. ANOMALY Detection

ANOMALY recall:

[PUT YOUR ACTUAL ANOMALY RECALL HERE]

This metric is useful because failing to detect an anomalous
telemetry condition could result in missed operational alerts.

## 12. Prediction Confidence

Average prediction confidence:

[PUT YOUR ACTUAL VALUE HERE]

## 13. Business Application

The ML prediction can provide an additional intelligence layer
for the AtmoSync monitoring and spoilage-risk workflow.

Predicted anomalies can be investigated before operational
actions are taken.

## 14. Important Limitation

The dataset is simulated and the condition labels originate
from the simulator's rule-based logic.

Therefore, the model demonstrates an ML workflow but its
performance should not be interpreted as validated real-world
anomaly-detection performance.

Actual deployment would require historical IoT telemetry with
independently observed operational outcomes.

## 15. Day 8 Deliverables

- ML training script
- Random Forest classification model
- ML prediction dataset
- Jupyter notebook
- Model evaluation
- Confusion matrix
- Feature importance analysis
- ML prediction report

## 16. Conclusion

Day 8 added a supervised machine learning layer to AtmoSync.
The system can now classify telemetry conditions as NORMAL,
WARNING, or ANOMALY and provide prediction confidence.

This creates the foundation for integrating predictive
analytics with the existing risk and spoilage arbitrage
decision engine.