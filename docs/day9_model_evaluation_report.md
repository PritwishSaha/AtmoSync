# Day 9 — Model Evaluation, Explainability & Error Analysis

## 1. Objective

The objective of Day 9 was to evaluate the AtmoSync condition prediction
model using a held-out test dataset, analyze prediction confidence,
identify classification errors, and understand which features contribute
most to the model's predictions.

---

## 2. Machine Learning Model

The AtmoSync condition prediction model uses a Random Forest Classifier.

### Model Configuration

- Algorithm: Random Forest Classifier
- Number of estimators: 200
- Random state: 42
- Class weighting: Balanced
- Target variable: `condition`
- Classes:
  - NORMAL
  - WARNING
  - ANOMALY

### Input Features

The model uses:

- Temperature
- Humidity
- Vibration
- Hour
- Day of week
- Commodity
- Container ID

Derived business-rule variables such as `spoilage_risk`,
`environmental_risk_score`, `recommended_action`, and
`arbitrage_opportunity` were excluded from the ML features to avoid
target leakage.

---

## 3. Train-Test Split

The dataset contains 1,785 telemetry records.

An 80/20 stratified train-test split was used.

| Dataset | Records |
|---|---:|
| Training | 1,428 |
| Testing | 357 |
| Total | 1,785 |

The test set was kept separate from model training and was used for
final performance evaluation.

---

## 4. Test Set Performance

The model achieved perfect classification performance on the held-out
test set.

| Metric | Result |
|---|---:|
| Accuracy | 100.00% |
| Weighted Precision | 100.00% |
| Weighted Recall | 100.00% |
| Weighted F1 Score | 100.00% |
| Anomaly Recall | 100.00% |
| Incorrect Predictions | 0 |
| Test Error Rate | 0.00% |

All 357 test records were classified correctly.

---

## 5. Confusion Matrix

The test-set confusion matrix was:

| Actual / Predicted | NORMAL | WARNING | ANOMALY |
|---|---:|---:|---:|
| NORMAL | 250 | 0 | 0 |
| WARNING | 0 | 70 | 0 |
| ANOMALY | 0 | 0 | 37 |

The matrix shows that no NORMAL, WARNING, or ANOMALY records were
misclassified in the held-out test set.

---

## 6. Prediction Confidence Analysis

The prediction confidence was analyzed using the maximum class
probability returned by the Random Forest model.

| Confidence Statistic | Value |
|---|---:|
| Mean confidence | 99.52% |
| Minimum confidence | 84.50% |
| Maximum confidence | 100.00% |
| Predictions below 90% | 2 |

The two predictions below 90% confidence were:

| Commodity | Container | Actual | Predicted | Confidence |
|---|---|---|---|---:|
| Banana | CONT_005 | NORMAL | NORMAL | 84.50% |
| Avocado | CONT_002 | NORMAL | NORMAL | 87.50% |

Both low-confidence predictions were nevertheless classified correctly.

---

## 7. Error Analysis

The held-out test set contained zero incorrect predictions.

- Test records: 357
- Incorrect predictions: 0
- Error rate: 0.00%

Therefore, there were no individual misclassified test records
requiring further error investigation.

However, the absence of errors on this simulated dataset should not
be interpreted as evidence that the model will achieve the same
performance on real-world telemetry.

---

## 8. Feature Importance

Random Forest feature importance was used to understand the relative
contribution of the input features.

### Top Features

| Feature | Importance |
|---|---:|
| Vibration | 58.06% |
| Temperature | 20.66% |
| Humidity | 17.59% |
| Hour | 0.76% |
| Commodity — Banana | 0.63% |
| Commodity — Avocado | 0.54% |
| Commodity — Mango | 0.34% |
| Commodity — Tomato | 0.31% |

The three primary sensor variables — vibration, temperature, and
humidity — account for approximately 96.31% of the total feature
importance.

Vibration has the highest model importance, followed by temperature
and humidity.

Feature importance indicates how the model uses the variables for
prediction. It does not establish that a feature causally produces a
particular container condition.

---

## 9. Sensor Analysis by Condition

Temperature, humidity, and vibration were analyzed across the
NORMAL, WARNING, and ANOMALY conditions.

Three visualizations were generated:

1. Average Vibration by Container Condition
2. Average Temperature by Container Condition
3. Average Humidity by Container Condition

These visualizations provide additional insight into the telemetry
patterns associated with the different condition classes.

---

## 10. Model Explainability

The feature-importance analysis indicates that the model relies
primarily on physical sensor measurements rather than contextual
variables.

The dominant features were:

- Vibration
- Temperature
- Humidity

Contextual variables such as hour, commodity, container ID, and day
of week had substantially lower importance in comparison.

---

## 11. Business Interpretation

For the AtmoSync pipeline, the ML model provides an automated method
for classifying container conditions from telemetry data.

The results can support the broader AtmoSync decision pipeline:

IoT Telemetry
→ Condition Prediction
→ Risk Analysis
→ Spoilage Assessment
→ Arbitrage Decision Support

The ML component can therefore act as an additional analytical layer
between raw telemetry and downstream operational decisions.

---

## 12. Important Limitation

The AtmoSync telemetry dataset used in this project is simulated.

The condition labels are structurally related to the telemetry
generation process. As a result, the perfect held-out test performance
may partly reflect patterns built into the simulated dataset.

Therefore, the results should be reported as:

**100% performance on the held-out test set**

rather than as evidence of 100% real-world model accuracy.

Real-world validation would require independently collected IoT
telemetry and observed container-condition outcomes.

---

## 13. Day 9 Deliverables

The following outputs were produced:

- `models/condition_prediction_model.pkl`
- `data/processed/ml_predictions.csv`
- `data/processed/feature_importance.csv`
- `data/processed/model_evaluation_summary.csv`
- `data/processed/sensor_statistics_by_condition.csv`
- `data/processed/sensor_means_by_condition.csv`
- `notebooks/day9_model_evaluation.ipynb`
- `docs/day9_model_evaluation_report.md`

---

## 14. Conclusion

Day 9 completed the evaluation and explainability stage of the
AtmoSync machine learning pipeline.

The Random Forest classifier correctly classified all 357 held-out
test records, achieving 100% accuracy, precision, recall, and F1
score, with 100% recall for the ANOMALY class.

Feature-importance analysis showed that vibration, temperature, and
humidity were the dominant predictive variables, collectively
accounting for approximately 96.31% of model feature importance.

The model evaluation demonstrates successful performance on the
simulated telemetry dataset while also highlighting the requirement
for real-world validation before operational deployment.