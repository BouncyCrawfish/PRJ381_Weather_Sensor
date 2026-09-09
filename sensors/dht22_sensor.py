"""
DHT22 temperature/humidity sensor driver (single GPIO data pin).

Install:
    sudo apt-get install -y libgpiod2
    pip3 install adafruit-circuitpython-dht --break-system-packages
"""

import board
import adafruit_dht

from config import DHT_DATA_PIN


class TempHumiditySensor:
    def __init__(self, pin=DHT_DATA_PIN):
        board_pin = getattr(board, f"D{pin}")
        self.device = adafruit_dht.DHT22(board_pin, use_pulseio=False)

    def read(self):
        """
        Returns a dict with temperature_c and humidity_pct.
        DHT sensors fail to read cleanly fairly often (that's normal for
        this sensor type) - if this raises RuntimeError, just try again
        on the next loop rather than treating it as a hardware fault.
        """
        temperature_c = self.device.temperature
        humidity_pct = self.device.humidity
        return {
            "temperature_c": round(temperature_c, 2) if temperature_c is not None else None,
            "humidity_pct": round(humidity_pct, 2) if humidity_pct is not None else None,
        }


if __name__ == "__main__":
    sensor = TempHumiditySensor()
    # DHT22 reads are flaky - retry a few times before giving up
    for attempt in range(5):
        try:
            print(sensor.read())
            break
        except RuntimeError as e:
            print(f"Read failed ({e}), retrying...")
