# Day 7 — Spoilage Arbitrage Decision Analytics

## 1. Objective

The objective of Day 7 was to convert micro-climate risk analytics into business-oriented intervention recommendations.

The decision engine uses environmental risk, spoilage-risk classification, sensor conditions, and anomaly indicators to recommend appropriate operational actions.

## 2. Decision Framework

The system maps spoilage risk to operational actions:

| Risk | Priority | Recommended Action |
|---|---|---|
| LOW | P4 | CONTINUE MONITORING |
| MEDIUM | P3 | INCREASE MONITORING |
| HIGH | P2 | CONSIDER REROUTING |
| CRITICAL | P1 | URGENT INTERVENTION |

## 3. Decision Results

The decision engine processed 1,785 telemetry records.

| Recommended Action | Records |
|---|---:|
| CONTINUE MONITORING | 890 |
| INCREASE MONITORING | 638 |
| CONSIDER REROUTING | 222 |
| URGENT INTERVENTION | 35 |

The results show that the majority of telemetry records require either continued or increased monitoring, while higher-risk records generate stronger intervention recommendations.

## 4. Potential Arbitrage Opportunities

The system identified 107 potential arbitrage opportunities.

This represents approximately 5.99% of the total telemetry records.

An arbitrage opportunity was flagged when a record was classified as HIGH or CRITICAL spoilage risk and had an environmental risk score of at least 6.

These records represent decision-support signals for potential intervention or rerouting.

## 5. Intervention Logic

The system uses the following operational logic:

- LOW risk → Continue monitoring
- MEDIUM risk → Increase monitoring
- HIGH risk → Consider rerouting
- CRITICAL risk → Urgent intervention

Additional environmental indicators such as temperature, humidity, vibration, and sensor anomalies are used to explain the decision.

## 6. Decision Score

A decision score was created using the environmental risk score together with additional environmental warning indicators.

Additional points may be contributed by:

- High temperature
- High humidity
- Elevated vibration
- Sensor anomaly

The score is used to prioritize records for investigation.

## 7. Business KPIs

Key Day 7 KPIs include:

- Total telemetry records: 1,785
- Potential arbitrage opportunities: 107
- Potential arbitrage rate: 5.99%
- HIGH-risk records: 222
- CRITICAL-risk records: 35
- Total intervention-required records: 257

## 8. Business Value

The decision engine converts raw environmental telemetry into operational recommendations.

Potential applications include:

- Risk-based shipment monitoring
- Prioritized intervention
- Rerouting consideration
- Automated alerts
- Future spoilage-cost optimization
- Supply-chain decision support

## 9. Important Limitation

The current telemetry dataset is simulated.

The project does not currently contain:

- Real market prices
- Alternative destination prices
- Rerouting costs
- Remaining shelf life
- Actual transportation constraints
- Observed physical spoilage outcomes

Therefore, the 107 arbitrage opportunities should be interpreted as analytical decision-support signals rather than confirmed financial arbitrage opportunities.

## 10. Day 7 Deliverables

- `scripts/spoilage_arbitrage.py`
- `data/processed/arbitrage_decisions.csv`
- `notebooks/day7_spoilage_arbitrage.ipynb`
- `docs/day7_spoilage_arbitrage_report.md`

## 11. Conclusion

Day 7 extended AtmoSync from micro-climate risk analytics to operational decision support.

The system processed 1,785 telemetry records and generated business-oriented recommendations ranging from continued monitoring to urgent intervention.

A total of 107 records were identified as potential arbitrage opportunities under the defined analytical rules.

This provides the foundation for future predictive modeling, financial arbitrage calculations, automated alerting, and dashboard development.