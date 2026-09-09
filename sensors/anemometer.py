"""
Anemometer (wind speed) driver - counts pulses on a GPIO pin over a fixed
sample window and converts to m/s using the cup-arm radius.

Install:
    pip3 install RPi.GPIO --break-system-packages
"""

import time
import math

import RPi.GPIO as GPIO

from config import (
    ANEMOMETER_PIN,
    PULSES_PER_REVOLUTION,
    ANEMOMETER_RADIUS_M,
    WIND_SAMPLE_SECONDS,
)


class Anemometer:
    def __init__(self, pin=ANEMOMETER_PIN):
        self.pin = pin
        self._pulse_count = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self._pulse_callback)

    def _pulse_callback(self, channel):
        self._pulse_count += 1

    def read(self, sample_seconds=WIND_SAMPLE_SECONDS):
        """
        Counts pulses for `sample_seconds`, then returns a dict with
        wind_speed_ms. Blocks for the duration of the sample window.
        """
        self._pulse_count = 0
        time.sleep(sample_seconds)
        pulses = self._pulse_count

        rotations = pulses / PULSES_PER_REVOLUTION
        rotations_per_second = rotations / sample_seconds

        # circumference of the circle traced by the cups
        circumference_m = 2 * math.pi * ANEMOMETER_RADIUS_M
        speed_ms = rotations_per_second * circumference_m

        return {"wind_speed_ms": round(speed_ms, 2)}

    def cleanup(self):
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup(self.pin)


if __name__ == "__main__":
    sensor = Anemometer()
    try:
        print("Spin the anemometer now...")
        print(sensor.read(sample_seconds=10))
    finally:
        sensor.cleanup()
