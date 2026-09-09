Project title

AtmoSync — Micro-Climate Arbitrage Analytics

Problem

Traditional supply-chain analytics rely on standard transit times and macro-weather forecasts and may fail to capture hyper-local environmental changes inside individual shipping containers. The project aims to monitor container conditions and identify potential spoilage and rerouting opportunities.

Main objective

Build an analytics system that combines:

IoT Container Telemetry
        +
Commodity Pricing
        ↓
Spoilage Analysis
        ↓
Spoilage Arbitrage
        ↓
Business Decision
Planned technologies

From the project specification:

Python
Apache Kafka
Snowflake
dbt
Apache Superset
SQL

The specified architecture uses Kafka for streaming ingestion, Snowflake for storage, dbt for transformation, and Superset for visualization.