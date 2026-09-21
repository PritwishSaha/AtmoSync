# Day 13 — Pipeline Architecture Report

## 1. Objective

The objective of Day 13 was to design a scalable data pipeline architecture for the AtmoSync micro-climate analytics platform.

The architecture connects telemetry generation, streaming ingestion, storage, transformation, analytics, machine learning, visualization, and business decision support.

---

## 2. Current System

The current AtmoSync implementation uses:

* Python
* Pandas
* CSV storage
* Machine Learning
* Risk Analytics
* Advanced Analytics
* Streamlit
* Plotly

The current implementation primarily follows a local batch-processing workflow.

---

## 3. Proposed Architecture

The proposed architecture is:

```text
IoT Simulator
      ↓
Apache Kafka
      ↓
Data Ingestion
      ↓
Raw Storage
      ↓
Snowflake
      ↓
dbt
      ↓
Analytics / ML
      ↓
Dashboard
      ↓
Spoilage Arbitrage Decision Support
```

The architecture separates data generation, ingestion, storage, transformation, analytics, visualization, and decision-support layers.

---

## 4. Streaming Layer

Apache Kafka is proposed as the streaming ingestion layer.

The proposed Kafka topic is:

`atmosync.telemetry`

Kafka is intended to decouple telemetry generation from downstream processing and support scalable event ingestion.

Kafka is currently part of the proposed architecture and has not been implemented as a production streaming cluster.

---

## 5. Warehouse Layer

Snowflake is proposed as the analytical data warehouse.

The planned warehouse structure includes:

* RAW
* STAGING
* ANALYTICS

The current AtmoSync implementation continues to use local files for analytical processing.

---

## 6. Transformation Layer

dbt is proposed as the transformation and data-modeling layer.

Expected responsibilities include:

* staging transformations
* data cleaning
* analytical models
* business metrics
* data quality tests
* documentation

The current transformations are primarily implemented using Python and Pandas.

---

## 7. Analytics Layer

The analytics layer contains:

* environmental risk analysis
* spoilage risk analysis
* anomaly detection
* ML condition prediction
* prediction monitoring
* advanced analytics
* operational priority analysis
* spoilage arbitrage decision support

The current project uses Python and machine-learning workflows for these analytical components.

---

## 8. Dashboard Layer

The current dashboard is implemented using:

* Streamlit
* Plotly

The dashboard presents telemetry monitoring, sensor analytics, spoilage-risk analytics, ML prediction monitoring, container analysis, commodity analysis, arbitrage decisions, and high-risk telemetry.

Apache Superset is included as a future BI option in the proposed architecture.

---

## 9. Local Pipeline Prototype

A Day 13 Python prototype was created at:

`pipeline/local_pipeline.py`

The prototype demonstrates:

1. Reading raw telemetry
2. Validating required columns
3. Checking missing values
4. Selecting pipeline fields
5. Writing processed pipeline output
6. Generating a pipeline summary

---

## 10. Validation Result

The local pipeline successfully processed:

* 1,785 telemetry records
* 5 containers
* 4 commodities
* 7 telemetry fields
* 0 missing values

The generated output is:

`data/processed/pipeline_sample.csv`

The validated output shape is:

`(1785, 7)`

---

## 11. Pipeline Configuration

Day 13 also introduced configuration and schema files.

### Telemetry Schema

`pipeline/schemas/telemetry_schema.json`

Schema version:

`1.0`

### Kafka Configuration

`pipeline/config/kafka_config.json`

### Pipeline Configuration

`pipeline/config/pipeline_config.json`

All three JSON configuration/schema files are intended to describe the proposed pipeline structure.

---

## 12. Architecture Diagram

The architecture diagram is stored at:

`architecture/atmosync_architecture.mmd`

It represents the proposed flow from the IoT simulator through Kafka, storage, Snowflake, dbt, analytics, machine learning, dashboard, and spoilage arbitrage decision support.

---

## 13. Current vs Future Architecture

The current system is primarily a local Python/Pandas batch-processing prototype.

The future architecture introduces:

* Apache Kafka for streaming
* Snowflake for analytical warehousing
* dbt for transformation
* scalable analytics infrastructure
* potential Apache Superset BI integration

Kafka, Snowflake, dbt, and Apache Superset should be considered architectural targets unless separately deployed and verified.

---

## 14. Limitations

The telemetry dataset is simulated.

Therefore, analytical findings demonstrate the project workflow rather than representing measurements from real shipping containers.

The current machine-learning results are also based on simulated telemetry and should not be interpreted as equivalent real-world model performance.

The spoilage-risk, arbitrage, and operational-priority rules are project-specific analytical decision-support mechanisms and have not been validated as real-world logistics or food-spoilage rules.

---

## 15. Day 13 Deliverables

* Pipeline architecture documentation
* Telemetry schema
* Kafka configuration
* Pipeline configuration
* Local pipeline prototype
* Architecture diagram
* Day 13 architecture report
* Pipeline sample dataset
* README architecture section
