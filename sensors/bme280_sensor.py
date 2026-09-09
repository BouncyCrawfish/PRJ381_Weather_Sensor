"""
BME280 temperature/humidity/pressure sensor driver (I2C).

The board was labelled GY-BMP280, but i2cdetect + the driver both
identified it as chip ID 0x60, which is a BME280 - the "E" version
adds a humidity sensor on top of what the BMP280 offers. So we get
temperature, pressure, AND humidity from this one sensor.

Install:
    pip3 install adafruit-circuitpython-bme280 --break-system-packages

Wiring (I2C):
    VCC -> Pi 3.3V (physical pin 1 or 17)
    GND -> Pi GND
    SCL -> Pi physical pin 5 (GPIO3)
    SDA -> Pi physical pin 3 (GPIO2)
    CSB, SDO -> left unconnected (fine as long as the board's onboard
                pull resistors put it in I2C mode at address 0x76 -
                confirmed via `sudo i2cdetect -y 1`)
"""

import board
import busio
import adafruit_bme280.basic as adafruit_bme280

from config import BME280_I2C_ADDRESS, SEA_LEVEL_PRESSURE_HPA


class TempHumidityPressureSensor:
    def __init__(self, address=BME280_I2C_ADDRESS):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.device = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=address)
        self.device.sea_level_pressure = SEA_LEVEL_PRESSURE_HPA

    def read(self):
        """Returns a dict with temperature_c, humidity_pct, pressure_hpa, altitude_m."""
        return {
            "temperature_c": round(self.device.temperature, 2),
            "humidity_pct": round(self.device.relative_humidity, 2),
            "pressure_hpa": round(self.device.pressure, 2),
            "altitude_m": round(self.device.altitude, 2),
        }


if __name__ == "__main__":
    sensor = TempHumidityPressureSensor()
    print(sensor.read())
