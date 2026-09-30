# Day 10 — ML Prediction Monitoring & Operational Insights

## 1. Objective

The objective of Day 10 was to extend the AtmoSync machine learning workflow beyond model prediction and evaluation into an operational monitoring layer.

During the previous stages, telemetry data was validated, transformed into machine-learning features, and processed through a Random Forest classification model. Day 10 focused on converting the resulting predictions into a structured monitoring dataset that can support operational analysis, dashboard development, and future alerting workflows.

The monitoring layer combines:

* Telemetry measurements
* Container identification
* Commodity information
* Actual condition labels
* Predicted condition labels
* Prediction confidence
* Confidence categories
* Prediction status
* Monitoring levels

The primary purpose of this layer is to make ML predictions easier to interpret from an operational perspective. Instead of treating a model prediction as an isolated output, the monitoring layer organizes predictions into actionable categories such as `NORMAL`, `MONITOR`, and `ANOMALY DETECTED`.

The Day 10 workflow therefore represents the transition from:

**Machine Learning Prediction → Operational Monitoring**

---

# 2. Data Source

The Day 10 analysis uses the complete ML prediction dataset generated during Day 8.

The monitoring dataset contains **1,785 telemetry records** collected from the simulated AtmoSync environment.

The dataset includes the following major fields:

| Category              | Fields                           |
| --------------------- | -------------------------------- |
| Identification        | Container ID                     |
| Time                  | Timestamp                        |
| Commodity             | Commodity                        |
| Sensor Data           | Temperature, Humidity, Vibration |
| Ground Truth          | Actual Condition                 |
| ML Output             | Predicted Condition              |
| Model Output          | Prediction Confidence            |
| Confidence Monitoring | Confidence Category              |
| Prediction Monitoring | Prediction Status                |
| Operations            | Monitoring Level                 |

The dataset was checked before analysis and **no missing values were identified** in the monitoring dataset.

This allowed the Day 10 analysis to be performed on the complete set of 1,785 telemetry records without requiring additional missing-value treatment.

---

# 3. Monitoring Dataset Structure

The Day 10 monitoring dataset was designed to combine raw operational information with machine-learning outputs.

Conceptually, each record represents:

> **One telemetry observation + its ML prediction + confidence information + operational monitoring classification**

For example, a telemetry record can contain temperature, humidity, and vibration measurements for a specific container and commodity. The ML model then predicts the condition of that observation. The prediction confidence is subsequently converted into a confidence category, and the predicted condition is converted into a monitoring level.

This structure makes the dataset suitable for downstream analytical applications such as:

* Power BI dashboards
* Apache Superset dashboards
* Alerting systems
* Container-level monitoring
* Commodity-level monitoring
* Model review workflows
* Future streaming monitoring

---

# 4. Predicted Condition Distribution

The Random Forest model generated predictions for all 1,785 telemetry records.

The predicted condition distribution was:

| Predicted Condition |   Records |  Percentage |
| ------------------- | --------: | ----------: |
| NORMAL              |     1,249 |      69.97% |
| WARNING             |       352 |      19.72% |
| ANOMALY             |       184 |      10.31% |
| **Total**           | **1,785** | **100.00%** |

The majority of telemetry records were classified as `NORMAL`.

A total of **352 records** were classified as `WARNING`, while **184 records** were classified as `ANOMALY`.

The predicted distribution matches the condition distribution represented in the simulated dataset.

This consistency is useful for validating the monitoring pipeline, but it should not by itself be interpreted as evidence that the model is performing perfectly. A proper model evaluation requires independent validation metrics such as the confusion matrix, precision, recall, F1-score, and validation/test-set performance.

---

# 5. Prediction Confidence Analysis

In addition to predicting the condition class, the ML model generated a confidence value for each prediction.

The overall mean prediction confidence was:

**0.995**

The minimum observed prediction confidence was:

**0.795**

This indicates that the model generally produced predictions with high confidence within the available simulated dataset.

However, model confidence should not automatically be interpreted as a statistically calibrated probability of correctness.

For example:

> A prediction confidence of 0.95 should not automatically be interpreted as meaning that the prediction has a 95% real-world probability of being correct.

Calibration would need to be evaluated separately using appropriate validation techniques.

---

# 6. Confidence Categorization

For operational monitoring, prediction confidence was divided into three categories.

The thresholds were defined as:

| Confidence Range         | Category          |
| ------------------------ | ----------------- |
| Confidence ≥ 0.90        | HIGH CONFIDENCE   |
| 0.75 ≤ Confidence < 0.90 | MEDIUM CONFIDENCE |
| Confidence < 0.75        | LOW CONFIDENCE    |

Using these operational thresholds, the resulting distribution was:

| Confidence Category |   Records |  Percentage |
| ------------------- | --------: | ----------: |
| HIGH CONFIDENCE     |     1,767 |      98.99% |
| MEDIUM CONFIDENCE   |        18 |       1.01% |
| LOW CONFIDENCE      |         0 |       0.00% |
| **Total**           | **1,785** | **100.00%** |

Therefore, almost the entire monitoring dataset fell into the high-confidence category.

Only **18 records** fell into the medium-confidence category, and no records were classified as low confidence under the defined threshold.

These thresholds are operational rules created for this monitoring workflow. They are not model-calibration thresholds and should be reviewed if the system is later deployed using real-world telemetry.

---

# 7. Monitoring Level Classification

The raw ML prediction labels were converted into operational monitoring levels.

The mapping was:

| Predicted Condition | Monitoring Level |
| ------------------- | ---------------- |
| NORMAL              | NORMAL           |
| WARNING             | MONITOR          |
| ANOMALY             | ANOMALY DETECTED |

The resulting monitoring distribution was:

| Monitoring Level |   Records |  Percentage |
| ---------------- | --------: | ----------: |
| NORMAL           |     1,249 |      69.97% |
| MONITOR          |       352 |      19.72% |
| ANOMALY DETECTED |       184 |      10.31% |
| **Total**        | **1,785** | **100.00%** |

This transformation makes the ML output easier to understand from an operational perspective.

Instead of exposing only technical prediction classes, the monitoring layer communicates the level of attention associated with each record.

---

# 8. Anomaly Monitoring

A total of:

**184 records**

were classified as `ANOMALY`.

The anomaly percentage was calculated as:

**184 / 1,785 × 100 = 10.31%**

Therefore:

> **10.31% of the complete simulated telemetry dataset was classified as anomalous by the ML monitoring layer.**

These anomaly records represent observations that the trained model classified as anomalous according to the available feature patterns.

They can later serve as inputs for:

* Dashboard anomaly indicators
* Operational review queues
* Alert generation
* Container-level investigation
* Commodity-level investigation
* Historical anomaly analysis
* Future real-time monitoring

However, an ML-predicted anomaly should not be interpreted as a confirmed physical failure or confirmed commodity spoilage event.

The current dataset is simulated, so these results demonstrate the monitoring architecture rather than real logistics performance.

---

# 9. Container-Level Anomaly Analysis

The monitoring dataset was further grouped by container to determine the proportion of predicted anomalies associated with each simulated container.

The results were:

| Container | Predicted Anomaly Rate |
| --------- | ---------------------: |
| CONT_005  |                 10.70% |
| CONT_001  |                 10.59% |
| CONT_002  |                 10.32% |
| CONT_003  |                 10.03% |
| CONT_004  |                  9.92% |

The difference between the highest and lowest observed anomaly rates is relatively small.

The highest observed rate was associated with:

**CONT_005 — 10.70%**

The lowest observed rate was:

**CONT_004 — 9.92%**

The relatively narrow range suggests that the simulated telemetry does not show a large difference in predicted anomaly frequency between the five containers.

However, these percentages should be treated strictly as descriptive statistics.

They should **not** be interpreted as evidence that one container is inherently more risky than another.

In a real production environment, container-level monitoring would ideally be performed over a larger historical dataset and would consider:

* Number of observations per container
* Operating duration
* Environmental conditions
* Sensor reliability
* Container equipment
* Route
* Location
* Commodity
* Seasonal conditions
* Maintenance history
* Historical incidents

This would allow persistent patterns to be distinguished from random variation.

---

# 10. Commodity-Level Anomaly Analysis

The monitoring dataset was also grouped by commodity to examine the distribution of predicted anomalies.

The resulting anomaly rates were:

| Commodity | Predicted Anomaly Rate |
| --------- | ---------------------: |
| Avocado   |                 11.99% |
| Mango     |                 10.85% |
| Banana    |                  9.90% |
| Tomato    |                  8.50% |

Among the four simulated commodities, Avocado had the highest observed predicted anomaly rate at **11.99%**, while Tomato had the lowest at **8.50%**.

The difference between these values is:

**11.99% − 8.50% = 3.49 percentage points**

These values provide a useful descriptive breakdown for dashboard development.

However, the difference should not be interpreted as evidence that Avocado is inherently more susceptible to spoilage or that Tomato is inherently safer.

Such conclusions would require real-world data containing validated spoilage outcomes, controlled environmental measurements, and appropriate statistical analysis.

The current results demonstrate how commodity-level monitoring can be implemented within the AtmoSync architecture.

---

# 11. Low-Confidence Prediction Analysis

Prediction confidence was also examined to identify records that may require additional review.

The minimum observed prediction confidence was:

**0.795**

Based on the operational threshold of 0.90, the dataset contained:

**18 records below the HIGH CONFIDENCE threshold.**

These records represent potentially useful review candidates.

In a production environment, low-confidence or medium-confidence predictions could trigger additional processing such as:

1. Requesting additional sensor measurements.
2. Checking sensor consistency.
3. Comparing the observation with recent telemetry.
4. Reviewing the container's recent history.
5. Checking related commodity conditions.
6. Sending the observation for human review.
7. Waiting for additional telemetry before triggering an operational intervention.

In the current dataset, the lowest-confidence observations were still classified correctly against the available labels.

However, this observation alone is not sufficient to establish general model reliability because the dataset is simulated and the number of low-confidence observations is small.

---

# 12. Relationship Between Model Features and Monitoring

Day 9 feature-importance analysis provided additional context for interpreting the model.

The dominant Random Forest features were:

| Feature        | Approximate Importance |
| -------------- | ---------------------: |
| Vibration      |                 58.06% |
| Temperature    |                 20.66% |
| Humidity       |                 17.59% |
| Other Features |                 ~3.70% |
| **Total**      |               **100%** |

The three primary sensor variables therefore accounted for approximately:

**96.30%**

of the model's feature importance.

This indicates that the trained Random Forest relied heavily on vibration, temperature, and humidity when producing its predictions.

However, feature importance should be interpreted carefully.

Feature importance describes the contribution of variables to the model's predictive behavior under the selected importance methodology. It does **not** establish that changing one of these variables directly causes an anomaly.

For example:

> High feature importance for vibration does not prove that vibration causes equipment failure or commodity spoilage.

A causal relationship would require additional experimental or observational analysis.

---

# 13. Vibration, Temperature and Humidity Monitoring

The Day 10 monitoring layer makes it possible to examine sensor values alongside ML predictions.

This is important because an operational monitoring system should not display the prediction independently from the underlying telemetry.

For example, a future dashboard could display:

* Current temperature
* Current humidity
* Current vibration
* Predicted condition
* Prediction confidence
* Container ID
* Commodity
* Timestamp
* Monitoring level

This allows an operator to understand both:

**What the model predicted**

and

**What sensor conditions were present when the prediction was generated.**

This combination is particularly useful for investigating anomalous records and understanding the context behind model predictions.

---

# 14. Operational Monitoring Logic

The Day 10 workflow can be represented as:

```text
Telemetry
    ↓
Data Validation
    ↓
Feature Engineering
    ↓
Machine Learning Model
    ↓
Condition Prediction
    ↓
Prediction Confidence
    ↓
Confidence Categorization
    ↓
Monitoring Classification
    ↓
Container Analysis
    ↓
Commodity Analysis
    ↓
Operational Monitoring
    ↓
Dashboard / Alerting
```

This architecture separates the machine-learning layer from the operational monitoring layer.

The ML model produces the prediction, while the monitoring layer converts that prediction into information that can be consumed by dashboards, analysts, or future alerting services.

---

# 15. Monitoring Dataset Generation

The Day 10 monitoring workflow was implemented using:

```text
scripts/create_prediction_monitoring.py
```

The script processes the ML prediction output and creates the structured monitoring dataset.

The resulting file is:

```text
data/processed/prediction_monitoring.csv
```

The workflow also produces a summary dataset:

```text
data/processed/day10_monitoring_summary.csv
```

The summary dataset can be used for reporting and dashboard preparation without repeatedly processing the complete telemetry dataset.

---

# 16. Notebook Analysis

The exploratory and analytical work was documented in:

```text
notebooks/day10_prediction_monitoring.ipynb
```

The notebook provides a reproducible environment for:

* Loading the prediction dataset
* Checking dataset dimensions
* Checking missing values
* Examining prediction distributions
* Calculating confidence statistics
* Categorizing confidence
* Calculating anomaly percentages
* Performing container-level analysis
* Performing commodity-level analysis
* Examining operational monitoring levels
* Preparing summary outputs

This separation between processing scripts and analytical notebooks helps maintain reproducibility.

The Python script performs the transformation, while the notebook provides the analysis and interpretation.

---

# 17. Dashboard Preparation

The Day 10 monitoring dataset provides the analytical foundation for the future AtmoSync dashboard.

The following KPIs can be generated directly from the monitoring data:

### 17.1 Total Telemetry Records

**1,785**

Represents the total number of telemetry observations currently included in the monitoring dataset.

### 17.2 Normal Records

**1,249**

Represents observations classified as `NORMAL`.

### 17.3 Warning / Monitor Records

**352**

Represents observations classified as `WARNING` and mapped to the `MONITOR` operational level.

### 17.4 Anomaly Records

**184**

Represents observations classified as `ANOMALY`.

### 17.5 Anomaly Percentage

**10.31%**

Represents the percentage of records classified as anomalous.

### 17.6 High-Confidence Predictions

**1,767**

Represents predictions with confidence greater than or equal to 0.90.

### 17.7 Medium-Confidence Predictions

**18**

Represents predictions with confidence between 0.75 and 0.90.

### 17.8 Low-Confidence Predictions

**0**

No predictions were below the defined 0.75 threshold.

### 17.9 Container Anomaly Rate

Can be displayed as a comparison across:

* CONT_001
* CONT_002
* CONT_003
* CONT_004
* CONT_005

### 17.10 Commodity Anomaly Rate

Can be displayed for:

* Avocado
* Mango
* Banana
* Tomato

These KPIs provide a direct bridge between the ML pipeline and the planned dashboard layer.

---

# 18. Recommended Dashboard Structure

The Day 10 dataset can support a dashboard with several sections.

### Section 1 — Overall Monitoring

Possible KPI cards:

```text
Total Records       1,785
Normal              1,249
Monitor               352
Anomalies             184
Anomaly Rate        10.31%
```

### Section 2 — Prediction Confidence

A visualization can show:

```text
HIGH       98.99%
MEDIUM      1.01%
LOW         0.00%
```

### Section 3 — Container Monitoring

A bar chart can compare predicted anomaly rates across containers.

### Section 4 — Commodity Monitoring

A bar chart can compare anomaly rates across commodities.

### Section 5 — Recent Anomalies

A table can display:

* Timestamp
* Container
* Commodity
* Temperature
* Humidity
* Vibration
* Predicted Condition
* Confidence
* Monitoring Level

### Section 6 — Sensor Monitoring

Charts can display temperature, humidity, and vibration trends over time.

This would allow operators to investigate whether anomalous predictions correspond with unusual sensor readings.

---

# 19. Potential Future Alerting Logic

The monitoring layer can later be extended into an alerting system.

A conceptual rule could be:

```text
IF Monitoring Level = ANOMALY DETECTED
    → Create anomaly event
```

A second rule could incorporate prediction confidence:

```text
IF Monitoring Level = ANOMALY DETECTED
AND Confidence < predefined threshold
    → Flag for additional review
```

Another possible approach would be to combine multiple telemetry observations:

```text
Single anomaly
        ↓
Review

Repeated anomalies
        ↓
Higher operational attention
```

This would be more appropriate for a production monitoring architecture than triggering a major intervention from a single simulated prediction.

The exact alert thresholds would need to be determined using real operational requirements and historical incident data.

---

# 20. Relationship With the Existing AtmoSync Architecture

Day 10 extends the existing AtmoSync pipeline.

The overall architecture can now be represented as:

```text
IoT / Simulated Telemetry
          ↓
Data Validation
          ↓
Feature Engineering
          ↓
Kafka / Data Ingestion
          ↓
Snowflake
          ↓
ML Prediction
          ↓
Prediction Confidence
          ↓
Monitoring Classification
          ↓
Container & Commodity Analysis
          ↓
Dashboard
          ↓
Future Alerting / Operational Workflow
```

This architecture demonstrates how machine-learning predictions can become part of a broader data engineering and analytics system.

The ML model is therefore not treated as an isolated notebook experiment.

Instead, its outputs are transformed into structured information that can be consumed by downstream systems.

---

# 21. Data Quality Considerations

The monitoring dataset contained no missing values, allowing all 1,785 records to participate in the analysis.

However, data completeness is only one component of monitoring data quality.

A production system would also need to monitor:

* Duplicate telemetry
* Sensor range violations
* Timestamp consistency
* Delayed telemetry
* Sensor outages
* Unexpected sensor spikes
* Container identification errors
* Commodity identification errors
* Model prediction failures
* Confidence distribution changes
* Data drift
* Feature drift
* Model performance degradation

These checks would become increasingly important if AtmoSync were connected to live IoT telemetry.

---

# 22. Model Monitoring Considerations

Day 10 primarily focuses on prediction monitoring rather than full model-performance monitoring.

A production implementation should eventually monitor both:

### Prediction Monitoring

* Prediction distribution
* Confidence distribution
* Anomaly frequency
* Container-level predictions
* Commodity-level predictions

### Model Performance Monitoring

* Accuracy
* Precision
* Recall
* F1-score
* Confusion matrix
* False positives
* False negatives
* Calibration
* Performance over time

This distinction is important.

A model can continue producing predictions while its real-world performance changes because of data drift or changes in operating conditions.

Therefore, future AtmoSync development should include a separate model-performance monitoring component.

---

# 23. Important Limitations

The Day 10 analysis has several important limitations.

### 23.1 Simulated Dataset

The telemetry data is simulated.

Therefore, the observed anomaly rates should not be interpreted as real logistics statistics.

### 23.2 Predicted Anomaly ≠ Confirmed Failure

An `ANOMALY` prediction represents a machine-learning classification.

It does not confirm:

* Equipment failure
* Sensor failure
* Commodity spoilage
* Physical damage
* Logistics disruption

### 23.3 No Causal Interpretation

The analysis does not establish that vibration, temperature, or humidity causes anomalies.

Feature importance only describes model behavior.

### 23.4 Confidence Is Not Calibration

The reported prediction confidence should not be interpreted as a calibrated probability of correctness.

Formal calibration analysis would be required before using confidence values for high-stakes operational decisions.

### 23.5 Operational Thresholds Are Designed Rules

The thresholds:

```text
≥ 0.90 → HIGH
0.75–0.90 → MEDIUM
< 0.75 → LOW
```

are operational monitoring rules created for this project.

They are not statistically validated production thresholds.

### 23.6 Limited Dataset Size

The current dataset contains 1,785 records.

A production monitoring system would ideally use a much larger and more diverse historical dataset.

### 23.7 Simulated Container and Commodity Patterns

Container-level and commodity-level differences may reflect characteristics of the simulated dataset rather than genuine operational behavior.

---

# 24. Day 10 Deliverables

The following components were completed during Day 10:

### Processing Script

```text
scripts/create_prediction_monitoring.py
```

Responsible for transforming ML predictions into the monitoring dataset.

### Monitoring Dataset

```text
data/processed/prediction_monitoring.csv
```

Contains telemetry information, ML predictions, confidence values, and operational monitoring classifications.

### Monitoring Summary

```text
data/processed/day10_monitoring_summary.csv
```

Contains aggregated monitoring statistics for reporting and future dashboard development.

### Analytical Notebook

```text
notebooks/day10_prediction_monitoring.ipynb
```

Contains the Day 10 exploratory analysis and monitoring calculations.

### Documentation

```text
docs/day10_prediction_monitoring_report.md
```

Contains the documented Day 10 methodology, findings, limitations, and operational interpretation.

---

# 25. Key Results Summary

| Metric                        | Result |
| ----------------------------- | -----: |
| Total telemetry records       |  1,785 |
| Normal predictions            |  1,249 |
| Warning predictions           |    352 |
| Anomaly predictions           |    184 |
| Predicted anomaly rate        | 10.31% |
| Mean prediction confidence    |  0.995 |
| Minimum prediction confidence |  0.795 |
| High-confidence predictions   |  1,767 |
| Medium-confidence predictions |     18 |
| Low-confidence predictions    |      0 |
| High-confidence percentage    | 98.99% |
| Medium-confidence percentage  |  1.01% |
| Low-confidence percentage     |  0.00% |

---

# 26. Overall Workflow Achievement

The main achievement of Day 10 was converting the machine-learning prediction output into an operationally structured monitoring layer.

Previously, the ML workflow primarily answered:

> **What condition does the model predict?**

Day 10 extended this question to:

> **How should the prediction be monitored and analyzed operationally?**

The resulting monitoring layer provides information about:

* What the model predicted
* How confident the model was
* Which monitoring category the prediction belongs to
* Which container generated the observation
* Which commodity was involved
* What the underlying sensor measurements were
* How anomaly rates vary across containers
* How anomaly rates vary across commodities

This creates a clear connection between machine learning and the broader AtmoSync data platform.

---

# 27. Conclusion

Day 10 successfully extended the AtmoSync machine-learning workflow from prediction into operational monitoring.

The monitoring layer processed **1,785 simulated telemetry records** and classified them into **1,249 NORMAL**, **352 WARNING**, and **184 ANOMALY** predictions.

The resulting anomaly rate was **10.31%**.

Prediction confidence was also incorporated into the monitoring workflow. The mean confidence was **0.995**, with **1,767 records (98.99%)** classified as high confidence and **18 records (1.01%)** classified as medium confidence. No observations fell below the defined low-confidence threshold.

Container-level and commodity-level analysis was performed to demonstrate how ML predictions can be aggregated for operational review. Container anomaly rates ranged from **9.92% to 10.70%**, while commodity anomaly rates ranged from **8.50% to 11.99%**.

The Day 10 work also incorporated the Day 9 feature-importance findings, where vibration, temperature, and humidity represented the dominant model features. These findings were treated as model-behavior observations rather than causal relationships.

Most importantly, the Day 10 workflow establishes a bridge between the **machine-learning layer** and the **operational dashboard layer** of AtmoSync.

The resulting architecture can now progress from:

**Telemetry → Validation → Feature Engineering → ML Prediction → Confidence → Monitoring → Dashboard → Future Alerting**

The current results should be considered a prototype demonstration using simulated telemetry. Before production deployment, the system would require validation against real operational data, model calibration, performance monitoring, data-drift detection, alert-threshold validation, and appropriate human-review workflows.

Overall, Day 10 establishes the analytical foundation required to transform AtmoSync ML predictions into a structured monitoring and decision-support component.
