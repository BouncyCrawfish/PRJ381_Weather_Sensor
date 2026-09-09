# IWOS Weather Station

A mobile weather-logging station built on a Raspberry Pi 5. It reads live
environmental data from onboard sensors, timestamps each reading, saves it
locally as a CSV backup, and publishes it over MQTT for remote/cloud use.

## Sensors
- **BME280** (I2C) — temperature, humidity, atmospheric pressure, altitude
- **Anemometer** (GPIO pulse counter) — wind speed
- **NEO-6M GPS** (UART) — latitude/longitude

## Features
- Configurable reading interval (default every 10s)
- Local CSV logging as a fallback if the network/broker is unavailable
- MQTT publishing to a configurable broker
- Onboard + external heartbeat LED to show the station is running
- Isolated test scripts for each sensor (`test_gps.py`, `check_gps.py`,
  `test_uart_loopback.py`, and running any sensor module directly with
  `python3 -m sensors.<name>`)

## Requirements
See `requirements.txt`. Run on Raspberry Pi OS with I2C and the hardware
UART serial port enabled via `raspi-config`.

## Usage
```bash
python3 main.py
```
Stop with Ctrl+C.
