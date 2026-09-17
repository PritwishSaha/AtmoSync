# Day 10 — ML Prediction Monitoring & Operational Insights

## 1. Objective

The objective of Day 10 was to transform the machine learning prediction output into an operational monitoring layer for the AtmoSync micro-climate analytics system.

The monitoring layer combines predicted condition, prediction confidence, sensor measurements, container information, and commodity information to support anomaly monitoring and operational review.

---

## 2. Data Source

The analysis uses the complete ML prediction dataset generated during Day 8.

The dataset contains 1,785 telemetry records and includes:

* Container ID
* Timestamp
* Commodity
* Temperature
* Humidity
* Vibration
* Actual condition
* Predicted condition
* Prediction confidence
* Confidence category
* Prediction status
* Monitoring level

No missing values were identified in the monitoring dataset.

---

## 3. Predicted Condition Distribution

The machine learning model generated the following predictions:

| Predicted Condition |   Records |
| ------------------- | --------: |
| NORMAL              |     1,249 |
| WARNING             |       352 |
| ANOMALY             |       184 |
| **Total**           | **1,785** |

The predicted condition distribution matches the condition labels in the simulated dataset.

---

## 4. Prediction Confidence Analysis

The mean prediction confidence was 0.995, while the minimum prediction confidence was 0.795.

Confidence was divided into three operational categories:

* HIGH CONFIDENCE: confidence >= 0.90
* MEDIUM CONFIDENCE: confidence >= 0.75 and < 0.90
* LOW CONFIDENCE: confidence < 0.75

The resulting distribution was:

| Confidence Category | Records | Percentage |
| ------------------- | ------: | ---------: |
| HIGH CONFIDENCE     |   1,767 |     98.99% |
| MEDIUM CONFIDENCE   |      18 |      1.01% |
| LOW CONFIDENCE      |       0 |      0.00% |

These confidence thresholds are operational monitoring rules and should not be interpreted as calibrated probability estimates.

---

## 5. Monitoring Levels

The model predictions were converted into monitoring-oriented labels.

The monitoring output contained:

| Monitoring Level | Records |
| ---------------- | ------: |
| NORMAL           |   1,249 |
| MONITOR          |     352 |
| ANOMALY DETECTED |     184 |

Normal predictions are treated as normal operational states.

Warning predictions are assigned to the monitoring category.

Anomaly predictions are flagged as ANOMALY DETECTED for further operational attention.

---

## 6. Anomaly Monitoring

A total of 184 records were predicted as ANOMALY.

This represents:

**10.31% of the complete 1,785-record dataset.**

The anomaly records can be used as an input to a future AtmoSync monitoring dashboard or alerting layer.

The current analysis is based on simulated telemetry and therefore does not represent confirmed real-world equipment failures or commodity spoilage.

---

## 7. Container-Level Anomaly Analysis

Predicted anomaly rates were calculated for each container.

| Container | Predicted Anomaly Rate |
| --------- | ---------------------: |
| CONT_005  |                 10.70% |
| CONT_001  |                 10.59% |
| CONT_002  |                 10.32% |
| CONT_003  |                 10.03% |
| CONT_004  |                  9.92% |

The anomaly rates are relatively close across the five simulated containers.

The rates should be interpreted as descriptive patterns in the generated telemetry rather than evidence of persistent container-level risk.

---

## 8. Commodity-Level Anomaly Analysis

Predicted anomaly rates were also calculated for each commodity.

| Commodity | Predicted Anomaly Rate |
| --------- | ---------------------: |
| Avocado   |                 11.99% |
| Mango     |                 10.85% |
| Banana    |                  9.90% |
| Tomato    |                  8.50% |

Avocado had the highest predicted anomaly rate in the simulated dataset, while Tomato had the lowest.

These differences are descriptive and should not be interpreted as evidence of real-world commodity spoilage risk without real operational data.

---

## 9. Low-Confidence Prediction Analysis

The complete monitoring dataset contained 18 predictions with confidence below 0.90.

The lowest prediction confidence observed was 0.795.

The lowest-confidence predictions were still classified correctly in the available dataset.

Low-confidence records can be used as review candidates in a production monitoring system, where additional sensor readings or human review could be considered.

---

## 10. Model and Sensor Interpretation

Day 9 feature importance analysis showed that the dominant model features were:

* Vibration: approximately 58.06%
* Temperature: approximately 20.66%
* Humidity: approximately 17.59%

Together, these three sensor variables accounted for approximately 96.30% of the model's feature importance.

The Day 10 analysis further examined vibration against prediction confidence and condition predictions.

Feature importance indicates how the trained Random Forest model used the variables for prediction. It does not establish a causal relationship between sensor measurements and anomalies.

---

## 11. Operational Monitoring Pipeline

The Day 10 monitoring layer extends the AtmoSync architecture:

IoT Telemetry
↓
Data Validation
↓
Feature Engineering
↓
Machine Learning Prediction
↓
Prediction Confidence
↓
Monitoring Classification
↓
Container and Commodity Analysis
↓
Operational Monitoring

This structure can later be connected to a dashboard and alerting system.

---

## 12. Dashboard Preparation

The Day 10 monitoring dataset provides several metrics that can be used in a future AtmoSync dashboard:

1. Total telemetry records
2. Normal records
3. Warning records
4. Anomaly records
5. Anomaly percentage
6. Prediction confidence
7. Container anomaly rate
8. Commodity anomaly rate
9. Low-confidence predictions
10. Current monitoring level

These outputs provide the analytical foundation for the dashboard layer planned in later project stages.

---

## 13. Important Limitations

The telemetry dataset used in AtmoSync is simulated.

Therefore:

* The results do not represent real-world logistics performance.
* Predicted anomalies are not confirmed equipment failures.
* Predicted anomalies are not confirmed commodity spoilage.
* The analysis does not establish causal relationships.
* Prediction confidence is not equivalent to calibrated probability.
* The confidence thresholds are operational rules created for monitoring.
* Real deployment would require validation against historical and live operational data.

The model should therefore be treated as a prototype decision-support component rather than a production-grade predictive system.

---

## 14. Day 10 Deliverables

The following components were completed:

* `scripts/create_prediction_monitoring.py`
* `data/processed/prediction_monitoring.csv`
* `data/processed/day10_monitoring_summary.csv`
* `notebooks/day10_prediction_monitoring.ipynb`
* `docs/day10_prediction_monitoring_report.md`

---

## 15. Conclusion

Day 10 extended the AtmoSync machine learning workflow from prediction and evaluation into operational monitoring.

The resulting monitoring dataset combines model predictions, confidence levels, sensor information, container information, and commodity information.

The analysis identified 184 predicted anomaly records within the 1,785-record simulated dataset, representing 10.31% of the records. Most predictions had high confidence, with 98.99% classified as HIGH CONFIDENCE.

Container-level and commodity-level anomaly rates were also generated, providing useful inputs for future dashboard development.

The Day 10 output establishes a monitoring layer that can be integrated with the AtmoSync dashboard and future alerting or data-pipeline components.
