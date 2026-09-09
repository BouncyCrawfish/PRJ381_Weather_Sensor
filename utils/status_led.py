"""
Status heartbeat LED - blinks BOTH the Pi 5's onboard ACT LED and an
external LED on GPIO, in sync, for as long as the station is running.

External LED wiring:
    anode (long leg)  -> ~330ohm resistor -> physical pin 13 (GPIO27)
    cathode (short leg) -> Pi GND (e.g. physical pin 14)
"""

import threading
import time

import RPi.GPIO as GPIO

from config import STATUS_LED_PIN, STATUS_LED_BLINK_INTERVAL_S

ACT_LED_PATH = "/sys/class/leds/ACT"


class StatusLED:
    def __init__(self, pin=STATUS_LED_PIN, interval=STATUS_LED_BLINK_INTERVAL_S):
        self.pin = pin
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

        self._write_act("trigger", "none")

    def _write_act(self, filename, value):
        try:
            with open(f"{ACT_LED_PATH}/{filename}", "w") as f:
                f.write(str(value))
        except PermissionError:
            raise PermissionError(
                "No permission to write to /sys/class/leds/ACT/ - "
                "check the udev rule was applied."
            )

    def _set_both(self, on: bool):
        GPIO.output(self.pin, GPIO.HIGH if on else GPIO.LOW)
        self._write_act("brightness", 1 if on else 0)

    def _blink_loop(self):
        state = False
        while not self._stop_event.is_set():
            state = not state
            self._set_both(state)
            time.sleep(self.interval)

    def start(self):
        if self._thread is not None:
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._blink_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=self.interval * 2)
            self._thread = None
        self._set_both(False)

    def cleanup(self):
        self.stop()
        GPIO.cleanup(self.pin)
        self._write_act("trigger", "mmc0")


if __name__ == "__main__":
    led = StatusLED()
    print(f"Blinking GPIO{led.pin} and the onboard ACT LED every {led.interval}s. Ctrl+C to stop.")
    led.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        led.cleanup()