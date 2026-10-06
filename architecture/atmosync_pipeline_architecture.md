# AtmoSync Pipeline Architecture

## 1. Overview

AtmoSync is a micro-climate analytics platform designed to monitor
temperature, humidity, and vibration data from commodity shipping
containers.

The platform analyzes telemetry data to identify environmental risk,
spoilage risk, anomalies, and potential spoilage arbitrage opportunities.

The proposed production-oriented architecture follows:

```text
IoT Simulator
      â†“
Apache Kafka
      â†“
Data Ingestion
      â†“
Raw Storage
      â†“
Snowflake
      â†“
dbt
      â†“
Analytics / ML
      â†“
Dashboard
      â†“
Business Decision Support
```

---

## 2. Architecture Layers

### Layer 1 â€” Data Generation

The Python IoT simulator generates telemetry records representing
sensor readings from shipping containers.

Main fields:

- container_id
- timestamp
- commodity
- temperature
- humidity
- vibration
- condition

Current implementation:

`simulator/iot_simulator.py`

---

### Layer 2 â€” Streaming Ingestion

Apache Kafka is implemented as the streaming ingestion component.

Kafka receives telemetry events from the IoT producer through the verified Kafka producer.

Verified topic:

`atmosync.telemetry`

Purpose:

- decouple data generation from downstream processing
- support streaming telemetry
- provide scalable event ingestion
- allow multiple consumers

---

### Layer 3 â€” Data Ingestion

A Kafka consumer will read telemetry events from the Kafka topic.

Responsibilities:

- consume telemetry messages
- validate message structure
- handle malformed records
- forward valid records to storage
- maintain ingestion metadata

---

### Layer 4 â€” Raw Data Storage

Raw telemetry should be preserved before analytical transformations.

The raw layer provides:

- data traceability
- reproducibility
- auditability
- recovery from transformation errors

Current local representation:

`data/raw/iot_telemetry.csv`

---

### Layer 5 â€” Data Warehouse

Snowflake is implemented and verified as the analytical data warehouse.

The warehouse will contain structured telemetry and analytical tables.

Potential layers:

- RAW
- STAGING
- ANALYTICS

---

### Layer 6 â€” dbt Transformation

dbt is implemented and verified for SQL-based transformation and data modeling.

Expected responsibilities:

- staging transformations
- data cleaning
- business metrics
- analytical models
- data quality tests
- documentation

---

### Layer 7 â€” Analytics and ML

The analytics layer calculates:

- environmental risk
- spoilage risk
- anomaly indicators
- prediction confidence
- operational priority
- arbitrage opportunities

Existing local analytics:

- feature engineering
- Random Forest condition prediction
- prediction monitoring
- advanced analytics
- spoilage arbitrage analysis

---

### Layer 8 â€” Dashboard

The dashboard presents operational analytics.

Current implementation:

`dashboard/app.py`

Current dashboard technology:

Streamlit + Plotly

Future architecture may use Apache Superset as the BI layer.

---

### Layer 9 â€” Business Decision Support

The final layer converts analytics into operational recommendations.

Example actions:

- CONTINUE MONITORING
- INCREASE MONITORING
- CONSIDER REROUTING
- URGENT INTERVENTION

These recommendations are analytical decision-support outputs and
should not be interpreted as validated real-world operational rules.

---

## 3. End-to-End Data Flow

```text
IoT Simulator
      |
      v
Kafka Producer
      |
      v
Kafka Topic
atmosync.telemetry
      |
      v
Kafka Consumer
      |
      v
Raw Storage
      |
      v
Snowflake RAW
      |
      v
dbt STAGING
      |
      v
dbt ANALYTICS
      |
      +----------------+
      |                |
      v                v
Risk Analytics       ML Layer
      |                |
      +-------+--------+
              |
              v
       Analytics Tables
              |
              v
          Dashboard
              |
              v
     Business Decisions
```

---

## 4. Data Flow Characteristics

### Batch Processing

The current implementation primarily processes telemetry using local
CSV files and Python/Pandas.

### Future Streaming Processing

The current implementation uses Apache Kafka for event-based ingestion. The production-oriented architecture can be extended to support continuous
telemetry ingestion.

### Raw Data Preservation

Raw telemetry should be preserved before transformation so that
downstream analytical results can be reproduced and investigated.

### Layered Processing

The architecture separates:

1. data generation
2. ingestion
3. storage
4. transformation
5. analytics
6. visualization
7. decision support

This separation allows individual components to evolve independently.

---

## 5. Reliability Considerations

A production AtmoSync pipeline should be designed to handle failures
without losing or corrupting telemetry data.

### Duplicate Events

The same telemetry event may be received more than once.

The pipeline should use a combination of:

- container_id
- timestamp
- event identifier

to detect duplicate events.

The existing validation layer already checks duplicate records in the
processed telemetry workflow.

### Malformed Records

Telemetry messages may contain invalid values or incorrect data types.

The ingestion layer should validate:

- required fields
- data types
- allowed condition values
- sensor ranges

Invalid records should be isolated instead of being allowed to
propagate into downstream analytical tables.

### Missing Sensor Values

Missing temperature, humidity, or vibration measurements can affect
risk calculations.

The pipeline should:

1. detect missing values
2. record the affected events
3. apply an appropriate handling strategy
4. monitor missing-value rates

### Schema Changes

Sensor systems may introduce new fields or modify existing fields.

The telemetry schema should therefore be versioned.

Current schema version:

`1.0`

### Late-Arriving Data

Telemetry may arrive later than its event timestamp because of
network or ingestion delays.

The warehouse and transformation layers should preserve the original
event timestamp and ingestion timestamp separately.

### Kafka Consumer Failure

If a Kafka consumer stops unexpectedly, the consumer should be able
to resume processing from its last committed offset.

Consumer groups and offset management help support this behavior.

### Warehouse Loading Failure

If data cannot be loaded into the warehouse, the failed records should
be retained for retry rather than being silently discarded.

### Transformation Failure

dbt transformations may fail because of invalid data, SQL errors, or
schema changes.

dbt tests and pipeline monitoring should identify these failures before
analytical outputs are consumed.

### Recovery Strategy

The pipeline should maintain:

- raw data
- processing logs
- validation results
- pipeline status
- retry mechanisms

This allows failed stages to be investigated and reprocessed.

---

## 6. Security Considerations

A production implementation should protect telemetry data,
warehouse credentials, and application configuration.

### Credential Management

Database and cloud credentials must not be stored directly in Python
source code or configuration files committed to Git.

Credentials should be provided through:

- environment variables
- `.env` files excluded from Git
- cloud secret-management services

### Database Access

Different pipeline components should use appropriate permissions.

For example:

- ingestion service â†’ write access to raw tables
- transformation service â†’ transformation permissions
- analytics service â†’ read access to analytical tables
- dashboard â†’ read-only access where possible

### Network Security

Connections between services should use encrypted communication where
supported.

### Git Security

Sensitive information must not be committed to the repository.

Examples include:

- passwords
- API keys
- access tokens
- private keys
- database credentials

### Environment Separation

Development and production environments should use separate credentials
and resources.

Example:

```text
Development
    â†“
Development Kafka
    â†“
Development Warehouse

Production
    â†“
Production Kafka
    â†“
Production Warehouse
```

This reduces the risk of development experiments affecting production
data.

---

## 7. Monitoring

A production data pipeline requires monitoring at each stage.

### Ingestion Metrics

The ingestion layer should monitor:

- messages received
- messages processed
- failed messages
- malformed messages
- duplicate events

### Kafka Metrics

Important Kafka metrics include:

- topic message rate
- consumer lag
- failed consumption attempts
- partition health

### Data Quality Metrics

The pipeline should monitor:

- missing values
- duplicate records
- invalid sensor values
- invalid condition labels
- schema validation failures

### Warehouse Metrics

The warehouse layer should monitor:

- records loaded
- failed loads
- loading latency
- table freshness

### dbt Metrics

The transformation layer should monitor:

- model execution status
- test failures
- transformation duration
- source freshness

### Analytics Metrics

The analytics layer should monitor:

- anomaly rate
- spoilage-risk distribution
- prediction confidence
- high-risk telemetry
- arbitrage opportunities

### Dashboard Monitoring

The dashboard should indicate whether the underlying analytical
datasets are current and available.

### Pipeline Health

A future pipeline monitoring dashboard could summarize:

```text
Pipeline Health
        |
        +-- Kafka
        |
        +-- Ingestion
        |
        +-- Warehouse
        |
        +-- dbt
        |
        +-- ML
        |
        +-- Dashboard
```

---

## 8. Current vs Planned Architecture

The current AtmoSync implementation contains both a verified
data-engineering pipeline and local analytical components.

The following components have been implemented and verified:

| Component | Current Status | Notes |
|---|---|---|
| IoT Simulator | Implemented | Generates simulated telemetry |
| CSV Validation | Implemented | Validates telemetry before ingestion |
| Feature Engineering | Implemented | Python-based analytical preprocessing |
| Apache Kafka | Implemented and verified | Topic: `telemetry` |
| Kafka Producer | Implemented and verified | Sends 1,785 validated telemetry records |
| Kafka Consumer | Implemented and verified | Reads Kafka events and loads Snowflake |
| Snowflake | Implemented and verified | `ATMOSYNC_DB.TELEMETRY_SCHEMA.RAW_TELEMETRY` |
| dbt | Implemented and verified | Staging, analytics models, and data-quality tests |
| Risk Analytics | Implemented | Environmental and spoilage-risk analysis |
| ML Prediction | Implemented | Condition prediction and monitoring |
| Spoilage Arbitrage | Implemented | Business decision-support logic |
| Streamlit Dashboard | Implemented | Operational analytics dashboard |
| Apache Superset | Not implemented | Future BI alternative |

### Verified Data Engineering Pipeline

The verified data-engineering flow is:

```text
IoT Simulator
      |
      v
Validated Telemetry
      |
      v
Kafka Producer
      |
      v
Kafka Topic: telemetry
      |
      v
Kafka Consumer
      |
      v
Snowflake RAW_TELEMETRY
      |
      v
dbt STAGING
      |
      v
dbt ANALYTICS
      |
      +-----------------------+
      |                       |
      v                       v
arbitrage_analysis     telemetry_summary

---

## 9. Important Limitations

### Simulated Telemetry

The current AtmoSync telemetry dataset is simulated.

Therefore, analytical findings should be interpreted as demonstrations
of the platform's analytical workflow rather than measurements of actual
shipping-container conditions.

### Local Batch Processing

The current implementation primarily processes CSV files using Python
and Pandas.

It is not yet a continuously running streaming pipeline.

### Kafka

Kafka has been implemented and verified as the streaming ingestion component.

The verified workflow uses the 	elemetry topic and a single-node local KRaft broker.

### Snowflake

Snowflake has been implemented and verified as the warehouse layer.

The verified raw telemetry table is ATMOSYNC_DB.TELEMETRY_SCHEMA.RAW_TELEMETRY and contains 1,785 records.

### dbt

dbt has been implemented and successfully verified against Snowflake.

The current transformations are implemented primarily through Python
and Pandas.

### Apache Superset

The current dashboard uses Streamlit and Plotly.

Superset is included as a future BI option in the architecture.

### Machine Learning

The condition-prediction model was developed using simulated telemetry.

Its performance on this dataset should not be interpreted as evidence
of equivalent performance on real-world sensor data.

### Decision Rules

The spoilage-risk and arbitrage rules are project-specific analytical
decision-support logic.

They have not been validated as real-world logistics or food-spoilage
rules.

### Priority Score

The operational priority score introduced in Day 12 is a project
analytics mechanism.

It should not be treated as a clinically, scientifically, or
industrially validated risk score.

### Production Readiness

The current project is a student analytics and data-engineering
prototype.

Additional work is required before production deployment, including:

- real IoT data
- streaming infrastructure
- cloud data warehouse
- authentication
- monitoring
- automated testing
- deployment
- security controls
- operational validation
