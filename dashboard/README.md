# AtmoSync Dashboard

## Overview

The AtmoSync Dashboard provides an interactive analytical view of simulated IoT telemetry from agricultural commodity containers.

The dashboard combines:

* Micro-climate sensor data
* Environmental risk analytics
* Spoilage risk classification
* Machine learning predictions
* Prediction confidence
* Container-level anomaly analysis
* Commodity-level anomaly analysis
* Spoilage arbitrage decisions

## Technology

* Python
* Pandas
* Streamlit
* Plotly

## Data Sources

The dashboard uses processed datasets generated during the AtmoSync analytics pipeline:

* `iot_telemetry_features.csv`
* `prediction_monitoring.csv`
* `arbitrage_decisions.csv`

## Run Locally

From the project root:

```bash
python -m streamlit run dashboard/app.py
```

The dashboard will be available through the local Streamlit server.

## Dashboard Sections

1. Condition Monitoring
2. Sensor Analytics
3. Spoilage Risk Analytics
4. ML Prediction Monitoring
5. Container-Level Analysis
6. Commodity-Level Analysis
7. Spoilage Arbitrage Decisions
8. High-Risk Telemetry

## Important Limitation

The current dashboard is based on simulated IoT telemetry. Risk and operational metrics should therefore be interpreted as analytical outputs from the simulated dataset rather than measurements of real-world spoilage or financial outcomes.
