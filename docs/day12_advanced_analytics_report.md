# Day 12 — Advanced Analytics Report

## Objective

The objective of Day 12 was to extend the AtmoSync analytics layer
with deeper container-level, commodity-level, time-based, sensor,
and operational-priority analysis.

## Analytical Inputs

The analysis uses:

- `iot_telemetry_features.csv`
- `prediction_monitoring.csv`
- `arbitrage_decisions.csv`

## Advanced Analytics

The Day 12 pipeline generates:

- Record-level advanced analytics
- Container risk profiles
- Commodity risk profiles
- Hourly risk profiles
- Daily risk profiles
- Operational priority scores

## Container-Level Analysis

Each container is analyzed using:

- Total telemetry records
- Predicted anomaly records
- Anomaly rate
- Warning records
- High-risk records
- Critical-risk records
- Average temperature
- Average humidity
- Average vibration
- Average environmental risk

## Commodity-Level Analysis

Each commodity is analyzed using:

- Total records
- Predicted anomalies
- Anomaly rate
- High-risk records
- Critical-risk records
- Average sensor values
- Average environmental risk

## Time-Based Analysis

Telemetry is analyzed by:

- Hour
- Date
- Anomaly rate
- High/critical risk rate
- Average sensor values
- Environmental risk

## Operational Priority

An analytical priority score was created by combining:

- Environmental risk
- Predicted condition
- Spoilage risk

The resulting levels are:

- NORMAL
- HIGH
- CRITICAL

The priority score is intended as a decision-support mechanism
for the simulated dataset.

## Key Analytical Outputs

The pipeline creates:

- `advanced_analytics.csv`
- `container_risk_profile.csv`
- `commodity_risk_profile.csv`
- `hourly_risk_profile.csv`
- `daily_risk_profile.csv`

## Limitations

The AtmoSync telemetry is simulated.

Therefore, observed relationships and patterns should not be
interpreted as causal real-world findings.

The operational priority score is a project-specific analytical
score and is not a validated production risk model.

ML prediction confidence should not automatically be interpreted
as a calibrated probability.

The arbitrage analysis is decision support and does not establish
a real financial arbitrage opportunity.