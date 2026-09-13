# Day 6 — Micro-Climate Risk & Spoilage Analytics

## 1. Objective

The objective of Day 6 was to analyze processed IoT telemetry data and identify micro-climate conditions associated with elevated spoilage risk across shipping containers and agricultural commodities.

The analysis used 1,785 telemetry records containing temperature, humidity, vibration, condition, environmental risk, and spoilage-risk features.

## 2. Risk Distribution

The spoilage-risk distribution was:

| Risk Level | Records |
|---|---:|
| LOW | 890 |
| MEDIUM | 638 |
| HIGH | 222 |
| CRITICAL | 35 |

There were 257 HIGH/CRITICAL records in total.

This indicates that approximately 14.4% of the telemetry records were classified as HIGH or CRITICAL spoilage risk.

## 3. Container Risk Analysis

Container-level analysis showed:

- CONT_004 had the highest average environmental risk at 2.942.
- CONT_003 followed with an average risk of 2.935.
- CONT_005 had the lowest average environmental risk at 2.818.
- CONT_004 recorded 51 HIGH-risk records and 5 CRITICAL records.

The relatively close average risk values indicate broadly similar simulated environmental conditions across containers.

## 4. Commodity Risk Analysis

Commodity-level analysis showed:

| Commodity | Avg Environmental Risk | HIGH | CRITICAL |
|---|---:|---:|---:|
| Banana | 3.159 | 67 | 6 |
| Avocado | 2.952 | 41 | 14 |
| Tomato | 2.821 | 46 | 6 |
| Mango | 2.689 | 68 | 9 |

Banana had the highest average environmental risk.

Avocado had the highest number of CRITICAL records, with 14.

## 5. Sensor Analysis

Average sensor values were compared between all records and HIGH/CRITICAL records.

| Sensor | Overall Average | HIGH/CRITICAL Average |
|---|---:|---:|
| Temperature | 11.23 | 12.32 |
| Humidity | 87.72 | 98.39 |
| Vibration | 0.191 | 0.362 |

HIGH/CRITICAL records were associated with higher temperature, substantially higher humidity, and higher vibration.

## 6. Time-Based Analysis

Environmental risk was aggregated hourly.

| Hour | Average Environmental Risk |
|---|---:|
| 17:00 | 2.879 |
| 18:00 | 2.895 |
| 19:00 | 3.015 |

The hourly analysis shows an increase in average environmental risk toward 19:00.

## 7. High-Risk Telemetry

A dedicated dataset was created containing all HIGH and CRITICAL telemetry records:

`data/processed/high_risk_telemetry.csv`

This dataset can be used for future alerting, anomaly investigation, and spoilage-arbitrage analysis.

## 8. Key Business Insights

1. 257 of 1,785 records were classified as HIGH or CRITICAL spoilage risk.
2. CONT_004 had the highest average environmental risk.
3. Banana had the highest average environmental risk among the analyzed commodities.
4. Avocado had the highest number of CRITICAL records.
5. HIGH/CRITICAL records showed higher average temperature, humidity, and vibration.
6. Average environmental risk increased from 2.879 at 17:00 to 3.015 at 19:00.
7. These insights can support future container monitoring and risk-based intervention.

## 9. Limitations

The telemetry dataset is simulated. The spoilage-risk categories are analytical indicators generated from environmental features and should not be interpreted as confirmed physical spoilage events.

No observed spoilage outcome was available in this dataset.

## 10. Day 6 Deliverables

- `notebooks/day6_microclimate_analysis.ipynb`
- `data/processed/high_risk_telemetry.csv`
- `data/processed/container_risk_summary.csv`
- `data/processed/commodity_risk_summary.csv`
- `docs/day6_microclimate_analysis_report.md`

## 11. Conclusion

Day 6 transformed the engineered telemetry dataset into actionable micro-climate risk insights. The analysis identified high-risk containers, commodities, sensor conditions, and time periods.

These outputs provide the analytical foundation for the next stage of AtmoSync: risk-based decision-making and spoilage-arbitrage analysis.