"""
Central configuration for the IWOS weather station.
Edit these values to match your wiring, sensor addresses, and cloud broker.

Wiring (Pi physical pin numbers you gave):
- DHT22 (temp/humidity): VCC -> pin 2 (5V), DATA -> pin 7 (GPIO4), GND -> pin 6 or 9
  NOTE: you mentioned "pin 11" for one of the DHT22 wires - pin 11 is GPIO17,
  which is already used by the wind sensor below. Double check your DHT22's
  data wire isn't actually on pin 11, or move the wind sensor to a free pin.
- Wind sensor (anemometer): one wire -> pin 11 (GPIO17), other wire -> pin 14 (GND)
- GPS (NEO-6M): VCC -> pin 1 (3.3V), GND -> pin 6, wired to the Pi's hardware
  UART (pins 8/10) rather than USB - see README for enabling the serial port.
"""

# ---------------- GPIO pins (BCM numbering) ----------------
ANEMOMETER_PIN = 17              # wind sensor pulse line -> physical pin 11 (GPIO17)

# ---------------- BME280 (temp/humidity/pressure, I2C) ----------------
# Confirmed on the bus via `sudo i2cdetect -y 1` at address 0x76.
# Chip ID 0x60 identifies this as a BME280 (has humidity), not a BMP280.
BME280_I2C_ADDRESS = 0x76
SEA_LEVEL_PRESSURE_HPA = 1013.25  # standard reference; adjust for local conditions if needed

# ---------------- Anemometer calibration ----------------
# Standard hobby 3-cup anemometer: 1 pulse per rotation (adjust to your datasheet)
PULSES_PER_REVOLUTION = 1
ANEMOMETER_RADIUS_M = 0.07       # radius of the cup arm in meters - measure yours
WIND_SAMPLE_SECONDS = 3          # how long to count pulses for one wind reading

#-----------------------LED---------------------------------------------------------------
             # heartbeat LED -> physical pin 13 (GPIO27)
STATUS_LED_BLINK_INTERVAL_S = 0.5  # on/off period while the station is running
STATUS_LED_PIN = 27              # external heartbeat LED -> physical pin 13 (GPIO27), through a resistor
# ---------------- GPS (NEO-6M, wired to Pi's hardware UART) ----------------
GPS_SERIAL_PORT = "/dev/ttyAMA0" # Pi's hardware UART (pins 8=TXD, 10=RXD)
GPS_BAUD_RATE = 9600             # NEO-6M default baud rate
GPS_READ_TIMEOUT_S = 2

# ---------------- Local data logging ----------------
CSV_LOG_PATH = "data/weather_log.csv"

# ---------------- MQTT / cloud publishing ----------------
MQTT_BROKER_HOST = "localhost"  # e.g. AWS IoT endpoint, HiveMQ, Mosquitto
MQTT_BROKER_PORT = 1883                                # 8883 if using TLS
MQTT_TOPIC = "iwos/weather"
MQTT_CLIENT_ID = "iwos-lead-vehicle-01"
MQTT_USE_TLS = False
MQTT_USERNAME = None             # set if your broker requires auth
MQTT_PASSWORD = None

# ---------------- Main loop ----------------
READING_INTERVAL_SECONDS = 10     # how often to take a full sensor reading
