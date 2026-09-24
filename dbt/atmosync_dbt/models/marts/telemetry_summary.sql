{{ config(materialized='table') }}

SELECT
    COUNT(*) AS total_readings,

    COUNT(DISTINCT container_id) AS total_containers,

    COUNT(DISTINCT commodity) AS total_commodities,

    ROUND(AVG(temperature), 2) AS avg_temperature,

    ROUND(MIN(temperature), 2) AS min_temperature,

    ROUND(MAX(temperature), 2) AS max_temperature,

    ROUND(AVG(humidity), 2) AS avg_humidity,

    ROUND(MIN(humidity), 2) AS min_humidity,

    ROUND(MAX(humidity), 2) AS max_humidity,

    ROUND(AVG(vibration), 3) AS avg_vibration,

    SUM(CASE WHEN condition = 'NORMAL' THEN 1 ELSE 0 END)
        AS normal_readings,

    SUM(CASE WHEN condition = 'WARNING' THEN 1 ELSE 0 END)
        AS warning_readings,

    SUM(CASE WHEN condition = 'ANOMALY' THEN 1 ELSE 0 END)
        AS anomaly_readings

FROM {{ ref('stg_telemetry') }}