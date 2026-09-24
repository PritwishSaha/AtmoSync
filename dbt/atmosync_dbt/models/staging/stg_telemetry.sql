{{ config(materialized='view') }}

SELECT
    container_id,
    timestamp,
    commodity,
    temperature,
    humidity,
    vibration,
    condition

FROM {{ source('telemetry', 'raw_telemetry') }}