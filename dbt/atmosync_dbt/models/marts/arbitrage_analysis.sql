{{ config(materialized='table') }}

SELECT
    container_id,
    timestamp,
    commodity,
    temperature,
    humidity,
    vibration,
    condition,

    CASE
        WHEN condition = 'ANOMALY'
             OR temperature < 0
             OR temperature > 20
             OR humidity > 95
             OR vibration > 0.40
        THEN 'HIGH RISK'

        WHEN condition = 'WARNING'
             OR temperature < 5
             OR temperature > 15
             OR humidity > 90
             OR vibration > 0.30
        THEN 'MEDIUM RISK'

        ELSE 'LOW RISK'
    END AS microclimate_risk,

    CASE
        WHEN condition = 'ANOMALY'
             OR temperature < 0
             OR temperature > 20
             OR humidity > 95
             OR vibration > 0.40
        THEN 'URGENT INTERVENTION'

        WHEN condition = 'WARNING'
             OR temperature < 5
             OR temperature > 15
             OR humidity > 90
             OR vibration > 0.30
        THEN 'CONSIDER REROUTING'

        ELSE 'CONTINUE MONITORING'
    END AS recommended_action

FROM {{ ref('stg_telemetry') }}