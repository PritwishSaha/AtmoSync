# AtmoSync - Day 5 Feature Engineering Report

## Objective

The objective of Day 5 was to transform validated IoT telemetry into an analysis-ready dataset through preprocessing and feature engineering.

## Input Dataset

Input file:

`data/validated/validated_telemetry.csv`

Records: **1,785**

Original features:

* container_id
* timestamp
* commodity
* temperature
* humidity
* vibration
* condition

## Preprocessing Performed

The following preprocessing operations were performed:

* Timestamp conversion
* Date extraction
* Hour extraction
* Day-of-week extraction
* Day-name extraction
* Temperature risk classification
* Humidity risk classification
* Vibration risk classification

## Feature Engineering

The following analytical features were created:

* temperature_deviation
* temperature_risk
* humidity_risk
* vibration_risk
* environmental_risk_score
* environmental_risk
* spoilage_risk

Additional container-level and commodity-level statistical features were also created.

## Container-Level Analysis

Container-level statistics were calculated for:

* Average temperature
* Maximum temperature
* Minimum temperature
* Average humidity
* Maximum humidity
* Minimum humidity
* Average vibration
* Maximum vibration
* Warning count
* Anomaly count
* Average environmental risk

### Container Risk Results

| Container | Average Environmental Risk |
| --------- | -------------------------: |
| CONT_004  |                      2.942 |
| CONT_003  |                      2.935 |
| CONT_002  |                      2.900 |
| CONT_001  |                      2.894 |
| CONT_005  |                      2.818 |

`CONT_004` had the highest average environmental risk score.

## Commodity-Level Analysis

Commodity-level statistics were generated for:

* Average temperature
* Average humidity
* Average vibration
* Warning count
* Anomaly count
* Average environmental risk

### Commodity Risk Results

| Commodity | Average Environmental Risk |
| --------- | -------------------------: |
| Banana    |                      3.159 |
| Avocado   |                      2.952 |
| Tomato    |                      2.821 |
| Mango     |                      2.689 |

`Banana` had the highest average environmental risk score.

## Spoilage Risk Distribution

| Spoilage Risk | Records |
| ------------- | ------: |
| LOW           |     890 |
| MEDIUM        |     638 |
| HIGH          |     222 |
| CRITICAL      |      35 |

The feature-engineering pipeline successfully classified all 1,785 telemetry records into spoilage-risk categories.

## Output Dataset

Output file:

`data/processed/iot_telemetry_features.csv`

Final dataset:

* Records: **1,785**
* Features: **35**

The processed dataset will be used for the next stage of AtmoSync analytics, spoilage-risk analysis, and arbitrage decision logic.

## Conclusion

Day 5 successfully transformed validated IoT telemetry into an analysis-ready feature dataset. The newly created temporal, sensor-risk, environmental-risk, spoilage-risk, container-level, and commodity-level features provide the foundation for container monitoring, spoilage analysis, and future arbitrage decision logic.

Thankyou