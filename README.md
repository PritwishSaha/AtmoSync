🌡️ AtmoSync — Micro-Climate Arbitrage Analytics

«Turning container-level environmental telemetry into actionable spoilage-risk and rerouting insights.»

AtmoSync is a micro-climate analytics and decision-support system designed for temperature-sensitive supply chains.

Traditional supply-chain analytics often depend on standard transit times, historical conditions, and macro-level weather information. However, the actual environment experienced by a commodity can vary significantly inside an individual shipping container.

AtmoSync addresses this gap by monitoring container-level telemetry such as temperature, humidity, and vibration, combining those signals with commodity information and analytical/ML outputs to identify potential spoilage risks and support spoilage arbitrage decisions.

---

📌 Project Overview

The core idea behind AtmoSync is:

IoT Container Telemetry
          +
Commodity Information
          ↓
Micro-Climate Analysis
          ↓
Condition / Spoilage Risk
          ↓
Arbitrage Analysis
          ↓
Operational Decision

Instead of asking only:

«"How long will the shipment take?"»

AtmoSync aims to answer:

«"What is happening to the commodity inside this specific container, and should the shipment continue, receive increased monitoring, be rerouted, or require intervention?"»

---

🎯 Problem Statement

Temperature-sensitive commodities such as fruits and vegetables can deteriorate when exposed to unfavorable environmental conditions.

A conventional supply-chain system may use:

- Expected transit duration
- Historical temperature
- Regional weather
- Fixed storage assumptions
- Average spoilage rates

These approaches may not capture container-specific micro-climate conditions.

For example:

Container A
Temperature: Normal
Humidity: Acceptable
Vibration: Low
        ↓
Continue Monitoring


Container B
Temperature: High
Humidity: High
Vibration: Elevated
        ↓
Potential Spoilage Risk
        ↓
Consider Rerouting

The objective of AtmoSync is therefore to create a data pipeline capable of monitoring these conditions at the individual container level.

---

💡 What is Micro-Climate Arbitrage?

Micro-Climate

A micro-climate is the localized environmental condition experienced within a specific area.

In AtmoSync, the micro-climate refers to environmental conditions inside a shipping container.

Important telemetry signals include:

- 🌡️ Temperature
- 💧 Humidity
- 📳 Vibration
- 📦 Container ID
- 🥭 Commodity
- 🕒 Timestamp
- ⚠️ Condition

---

Arbitrage

In this project, arbitrage refers to identifying an operational opportunity where changing the shipment decision may reduce potential spoilage-related loss.

For example:

Shipment
   ↓
Container condition deteriorates
   ↓
Higher spoilage risk
   ↓
Potential economic loss
   ↓
Evaluate alternative action
   ↓
Continue / Monitor / Reroute / Intervene

The system does not simply detect an anomaly.

It attempts to connect:

Environmental Condition
          +
Commodity
          +
Risk
          ↓
Operational Decision

---

🎯 Main Objective

The primary objective of AtmoSync is to build an analytics pipeline that combines:

1. IoT Container Telemetry

Environmental measurements collected from simulated shipping containers.

2. Commodity Information

Information about the commodity being transported.

3. Condition Analysis

Classification of container conditions into operational states.

4. ML Prediction Monitoring

Monitoring predicted conditions and prediction confidence.

5. Spoilage-Risk Analysis

Identifying conditions that may indicate increased spoilage risk.

6. Arbitrage Decision Support

Converting analytical results into operational actions such as:

- Continue monitoring
- Increase monitoring
- Consider rerouting
- Urgent intervention

---

🏗️ System Architecture

The high-level AtmoSync architecture is:

                    ┌───────────────────┐
                    │   IoT Simulator   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Apache Kafka    │
                    │ Streaming Layer   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Raw Telemetry  │
                    │      Data        │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     Snowflake    │
                    │ Data Warehouse    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │       dbt        │
                    │ Transformation    │
                    └─────────┬─────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │     Analytics + ML       │
                │ Prediction & Monitoring  │
                └────────────┬─────────────┘
                             │
                             ▼
                    ┌───────────────────┐
                    │ Apache Superset   │
                    │    Dashboard      │
                    └─────────┬─────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │ Spoilage Arbitrage       │
                │ Decision Support         │
                └──────────────────────────┘

---

🔄 Data Flow

AtmoSync follows a layered data engineering architecture.

Layer 1 — Data Generation

An IoT-style simulator generates container telemetry.

Example:

container_id = CONT_001
timestamp    = 2026-09-10 10:30:00
commodity    = Avocado
temperature  = 14.2
humidity     = 88.4
vibration   = 0.18

---

Layer 2 — Streaming

Apache Kafka acts as the streaming ingestion layer.

IoT Simulator
      ↓
Kafka Producer
      ↓
Kafka Topic
      ↓
Kafka Consumer

This allows telemetry to be handled as a stream instead of treating every record as an isolated file.

---

Layer 3 — Raw Data

Telemetry data is captured before analytical transformations.

The raw dataset contains:

container_id
timestamp
commodity
temperature
humidity
vibration
condition

---

Layer 4 — Snowflake

Snowflake provides the analytical data warehouse.

The project uses:

Database:
ATMOSYNC_DB

Schema:
TELEMETRY_SCHEMA

Raw Table:
RAW_TELEMETRY

The raw telemetry is loaded into Snowflake before downstream transformation.

---

🧹 Data Validation

Before analytical processing, the telemetry dataset is validated.

Validation includes checks for:

- Missing values
- Duplicate records
- Invalid sensor values
- Data types
- Condition values
- Temperature ranges
- Humidity values
- Vibration measurements

The validated dataset contains 1,785 records.

Dataset Summary

Metric| Value
Total records| 1,785
Columns| 7
Containers| 5
Commodities| 4
Missing values| 0
Duplicate records| 0
Invalid sensor records| 0

---

📊 Dataset Structure

The main telemetry dataset contains seven columns.

Column| Description
"container_id"| Unique shipping container identifier
"timestamp"| Time at which telemetry was recorded
"commodity"| Commodity being transported
"temperature"| Container temperature
"humidity"| Container humidity
"vibration"| Measured vibration level
"condition"| Operational condition classification

Example:

container_id| timestamp| commodity| temperature| humidity| vibration| condition
CONT_001| 2026-09-10 10:00| Avocado| 11.2| 86.4| 0.18| NORMAL
CONT_002| 2026-09-10 10:05| Mango| 16.7| 91.2| 0.24| WARNING
CONT_003| 2026-09-10 10:10| Banana| 19.4| 94.1| 0.31| ANOMALY

---

📈 Dataset Statistics

The dataset contains four commodities:

Commodity| Records
Mango| 470
Tomato| 459
Avocado| 442
Banana| 414

Condition distribution:

Condition| Records
NORMAL| 1,249
WARNING| 352
ANOMALY| 184

---

🌡️ Sensor Statistics

Temperature

Mean: 11.228
Minimum: -1.98
Maximum: 20.93

Humidity

Mean: 87.715

Vibration

Mean: 0.191

These variables form the primary environmental signals used for monitoring container conditions.

---

🧠 Condition Classification

AtmoSync uses operational condition categories:

NORMAL
   ↓
WARNING
   ↓
ANOMALY

These categories provide a simplified operational interpretation of sensor conditions.

The system can therefore move from raw numerical measurements:

Temperature = 18.4
Humidity    = 93.1
Vibration   = 0.29

to an operational state:

ANOMALY

This makes the telemetry easier to interpret for downstream analytics and decision support.

---

🤖 ML Prediction Monitoring

The project also includes an ML prediction monitoring layer.

The monitoring dataset contains:

- Actual condition
- Predicted condition
- Prediction confidence
- Confidence category
- Prediction status
- Monitoring level
- Sensor measurements
- Container information
- Commodity information

The purpose is not only to generate a prediction but also to monitor how reliable that prediction is.

Conceptually:

Sensor Data
     ↓
ML Model
     ↓
Prediction
     +
Confidence
     ↓
Monitoring Layer

---

📊 Prediction Monitoring

Prediction confidence is categorized to make ML output easier to interpret.

The monitoring layer combines:

Predicted Condition
        +
Prediction Confidence
        +
Sensor Measurements
        +
Container
        +
Commodity

This creates an operational monitoring view rather than exposing raw model output alone.

---

🚚 Spoilage Arbitrage Decision Layer

The monitoring system translates analytical signals into potential operational actions.

Current action categories include:

Action| Records
CONTINUE MONITORING| 890
INCREASE MONITORING| 638
CONSIDER REROUTING| 222
URGENT INTERVENTION| 35

Conceptually:

                  Telemetry
                     ↓
              Condition Analysis
                     ↓
               ML Monitoring
                     ↓
               Risk Evaluation
                     ↓
        ┌────────────┼─────────────┐
        ↓            ↓             ↓
    Continue      Monitor       Reroute
   Monitoring     Closely       /Intervene

These categories are intended as decision-support outputs, not automatic commands to physically reroute a shipment.

---

❄️ Why Container-Level Monitoring Matters

Consider two containers transporting the same commodity.

Container A

Temperature → Stable
Humidity    → Stable
Vibration   → Low
Condition   → NORMAL

Possible operational interpretation:

Continue Monitoring

Container B

Temperature → Increasing
Humidity    → High
Vibration   → Elevated
Condition   → ANOMALY

Possible interpretation:

Increase Monitoring
          ↓
Evaluate Spoilage Risk
          ↓
Consider Rerouting

The important insight is that the two shipments may have the same planned route and transit duration while experiencing different internal conditions.

---

🏢 Snowflake Data Warehouse

AtmoSync uses Snowflake as the central analytical warehouse.

Current configuration:

Database
└── ATMOSYNC_DB
    └── TELEMETRY_SCHEMA
        └── RAW_TELEMETRY

The warehouse provides centralized storage for downstream transformation and analytics.

---

🔧 dbt Transformation Layer

dbt is used to transform and test warehouse data.

The dbt project currently includes:

Source
  ↓
stg_telemetry
  ↓
Analytics Models

The staging layer standardizes the raw telemetry before analytical use.

Example architecture:

Snowflake RAW_TELEMETRY
          ↓
       dbt Source
          ↓
   stg_telemetry
          ↓
   Analytics Models
          ↓
 Dashboard / Analysis

The dbt workflow includes:

- Sources
- Models
- SQL transformations
- Data tests
- Build execution

---

🧪 Data Quality Testing

Data quality is an important part of the pipeline.

The dbt project includes tests covering the warehouse data model.

The pipeline verifies that transformed data satisfies expected structural and quality conditions before being used downstream.

Conceptually:

Raw Data
   ↓
Transformation
   ↓
Tests
   ↓
Pass
   ↓
Analytics

If a test fails:

Raw Data
   ↓
Transformation
   ↓
Test Failure
   ↓
Investigate Data

---

📊 Apache Superset

Apache Superset is used as the visualization and dashboard layer.

The dashboard is intended to expose operational insights from the AtmoSync data pipeline.

Potential dashboard sections include:

1. Container Overview

Total Containers
Active Containers
Normal Containers
Warning Containers
Anomalous Containers

2. Environmental Monitoring

Charts for:

- Temperature
- Humidity
- Vibration

3. Condition Distribution

NORMAL
WARNING
ANOMALY

4. Commodity Analysis

Compare environmental conditions across:

- Avocado
- Banana
- Mango
- Tomato

5. Arbitrage Monitoring

Display:

Continue Monitoring
Increase Monitoring
Consider Rerouting
Urgent Intervention

---

🛠️ Technology Stack

Technology| Purpose
Python| Data generation, processing and analytics
Pandas| Data manipulation
NumPy| Numerical operations
Apache Kafka| Streaming ingestion
Snowflake| Cloud data warehouse
SQL| Data querying and transformation
dbt| Data transformation and testing
ML| Condition prediction and monitoring
Apache Superset| Dashboard and visualization
Git| Version control
GitHub| Source-code management
Docker| Containerized services

---

🧰 Tools by Pipeline Stage

DATA GENERATION
      ↓
    Python
      ↓
STREAMING
      ↓
 Apache Kafka
      ↓
DATA STORAGE
      ↓
  Snowflake
      ↓
TRANSFORMATION
      ↓
     dbt
      ↓
ANALYTICS / ML
      ↓
 Python / ML
      ↓
VISUALIZATION
      ↓
Apache Superset
      ↓
DECISION SUPPORT

---

📁 Project Structure

A recommended repository structure is:

AtmoSync/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── warehouse/
│
├── kafka/
│   ├── producer.py
│   └── consumer.py
│
├── ml/
│   ├── prediction.py
│   └── monitoring.py
│
├── dbt/
│   └── atmosync/
│       ├── models/
│       ├── tests/
│       ├── macros/
│       ├── dbt_project.yml
│       └── profiles.yml
│
├── analytics/
│   └── analysis.py
│
├── dashboard/
│   └── ...
│
├── reports/
│
├── requirements.txt
├── README.md
└── .gitignore

«The exact folder structure may differ from the current repository; the structure above represents a clean organization for the complete pipeline.»

---

🚀 Pipeline Execution

1. Create Python Environment

python -m venv .venv

Activate on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

---

2. Install Dependencies

pip install -r requirements.txt

Example dependencies:

pandas
numpy
kafka-python

Additional packages may be required depending on the analytics, ML, database, and dashboard components being executed.

---

⚡ Running Kafka

AtmoSync uses Apache Kafka as the streaming layer.

The Kafka setup uses KRaft mode, eliminating the need for a separate ZooKeeper service.

Conceptually:

Python Producer
      ↓
Kafka Broker
      ↓
Kafka Topic
      ↓
Python Consumer

Telemetry messages can be published to Kafka and consumed downstream.

---

❄️ Snowflake Setup

Create the AtmoSync database and schema:

CREATE DATABASE ATMOSYNC_DB;

CREATE SCHEMA ATMOSYNC_DB.TELEMETRY_SCHEMA;

The raw telemetry table is then used for ingestion:

ATMOSYNC_DB
    ↓
TELEMETRY_SCHEMA
    ↓
RAW_TELEMETRY

---

🔨 dbt Setup

Install dbt with the Snowflake adapter:

pip install dbt-core dbt-snowflake

Check installation:

dbt --version

Move into the dbt project:

cd dbt/atmosync

Run the project:

dbt build

The build process performs:

Models
+
Tests
+
Sources
↓
Build Result

---

📊 Dashboard

Apache Superset provides the visualization layer.

The dashboard can connect to the transformed Snowflake data and expose:

Container Monitoring
        +
Sensor Trends
        +
Condition Distribution
        +
ML Predictions
        +
Prediction Confidence
        +
Arbitrage Actions

---

📌 Key Metrics

AtmoSync can monitor metrics such as:

Container Metrics

- Total containers
- Container-wise condition
- Container-wise telemetry
- Anomaly count

Environmental Metrics

- Average temperature
- Maximum temperature
- Minimum temperature
- Average humidity
- Average vibration

Commodity Metrics

- Commodity distribution
- Commodity-wise anomalies
- Commodity-wise environmental conditions

ML Metrics

- Predicted condition
- Prediction confidence
- Confidence category
- Prediction status

Operational Metrics

- Continue monitoring
- Increase monitoring
- Consider rerouting
- Urgent intervention

---

📈 Example Analytical Questions

AtmoSync can be used to answer questions such as:

Container Analysis

«Which containers are currently showing abnormal conditions?»

Temperature Analysis

«Which containers experienced the highest temperature?»

Commodity Analysis

«Which commodities are associated with more warning/anomaly records?»

Sensor Analysis

«How does humidity vary across containers?»

ML Analysis

«Where are model predictions showing lower confidence?»

Operational Analysis

«How many records require increased monitoring?»

Arbitrage Analysis

«Which records should be evaluated for possible rerouting?»

---

🔍 Example End-to-End Scenario

Consider an avocado shipment:

Commodity
   ↓
Avocado

Container
   ↓
CONT_003

Telemetry
   ↓
Temperature = 18.5°C
Humidity    = 94%
Vibration   = 0.32

The pipeline processes the record:

IoT Telemetry
      ↓
Kafka
      ↓
Snowflake
      ↓
dbt
      ↓
Analytics
      ↓
ML Monitoring
      ↓
Risk / Condition Analysis
      ↓
Operational Action

The resulting monitoring layer may classify the shipment into an action such as:

CONSIDER REROUTING

The purpose is to provide an analyst or supply-chain operator with an additional signal for decision-making.

---

🧩 Engineering Concepts Demonstrated

This project demonstrates several practical data-engineering and analytics concepts.

Data Engineering

- Data ingestion
- Streaming pipelines
- Data validation
- Data warehousing
- ETL/ELT
- Data transformation
- Data quality testing

Analytics

- Exploratory data analysis
- Descriptive statistics
- Aggregation
- Trend analysis
- Condition analysis
- Operational analytics

Machine Learning

- Prediction generation
- Prediction confidence
- Model monitoring
- Prediction status
- Operational interpretation

Data Visualization

- KPI dashboards
- Time-series analysis
- Distribution analysis
- Operational monitoring

DevOps / Engineering

- Docker
- Git
- GitHub
- Environment management
- Reproducible development

---

🔐 Data Quality Principles

AtmoSync follows several data-quality principles:

Accuracy
   +
Completeness
   +
Consistency
   +
Validity
   +
Traceability

The telemetry dataset was checked for:

Missing Values → 0
Duplicates     → 0
Invalid Sensor Data → 0

This validation provides a cleaner foundation for downstream analytics.

---

🔮 Future Improvements

Potential extensions include:

1. Real IoT Hardware

Replace the simulator with real sensors.

Temperature Sensor
Humidity Sensor
Vibration Sensor
       ↓
IoT Gateway
       ↓
Kafka

---

2. Real-Time Streaming Dashboard

Instead of periodic analysis:

Sensor
  ↓
Kafka
  ↓
Snowflake
  ↓
Dashboard

could support near-real-time monitoring.

---

3. Commodity Price Integration

Add external commodity pricing data:

Container Telemetry
        +
Commodity Market Price
        ↓
Economic Impact
        ↓
Arbitrage Analysis

This would make the "arbitrage" component more explicitly economic rather than primarily operational.

---

4. Advanced Spoilage Prediction

Future versions could estimate:

Spoilage Probability
       +
Expected Loss
       +
Rerouting Cost
       ↓
Economic Decision Support

---

5. Automated Alerts

The system could generate alerts when:

Temperature > Threshold
        OR
Humidity > Threshold
        OR
Vibration > Threshold
        OR
Prediction Confidence < Threshold

Example:

⚠️ Container CONT_004

Condition: ANOMALY
Temperature: 19.2°C
Humidity: 