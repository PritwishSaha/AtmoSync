# AtmoSync IoT Telemetry Data Dictionary

## Purpose

This document defines the structure of the IoT telemetry data
used by the AtmoSync Micro-Climate Arbitrage Analytics system.

## IoT Telemetry Fields

| Column | Data Type | Description |
|---|---|---|
| container_id | String | Unique identifier of the shipping container |
| timestamp | DateTime | Time at which the sensor reading was recorded |
| temperature | Float | Temperature inside the container in °C |
| humidity | Float | Relative humidity inside the container in % |
| vibration | Float | Vibration level detected by the container sensor |
| latitude | Float | Current geographic latitude of the container |
| longitude | Float | Current geographic longitude of the container |
| commodity | String | Agricultural commodity being transported |
| origin | String | Shipment origin |
| destination | String | Shipment destination |