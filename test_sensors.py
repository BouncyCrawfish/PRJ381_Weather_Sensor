"""
Simple test script - reads the DHT22 (temp/humidity), anemometer (wind),
and GPS, and prints the results.

Run this from inside the iwos_weather_station folder:
    python3 test_sensors.py

Each sensor is wrapped in its own try/except, so if one sensor has a wiring
problem, you'll still see results (or a clear error) for the other two,
instead of the whole script crashing on the first failure.
"""

from sensors.dht22_sensor import TempHumiditySensor
from sensors.anemometer import Anemometer
from sensors.gps_reader import GPSReader


def test_temperature_humidity():
    print("\n--- Temperature / Humidity (DHT22) ---")
    try:
        sensor = TempHumiditySensor()
        # DHT22 reads are flaky - retry a few times before giving up
        for attempt in range(5):
            try:
                reading = sensor.read()
                print("SUCCESS:", reading)
                break
            except RuntimeError as e:
                print(f"  retry {attempt + 1}/5 after read error: {e}")
        else:
            print("FAILED: no good reading after 5 attempts")
    except Exception as e:
        print("FAILED:", e)


def test_wind():
    print("\n--- Wind Speed (Anemometer) ---")
    try:
        sensor = Anemometer()
        print("Spin the anemometer now, measuring for 10 seconds...")
        reading = sensor.read(sample_seconds=10)
        print("SUCCESS:", reading)
        sensor.cleanup()
    except Exception as e:
        print("FAILED:", e)


def test_gps():
    print("\n--- GPS ---")
    try:
        sensor = GPSReader()
        print("Waiting for GPS fix (can take up to a minute outdoors)...")
        reading = sensor.read()
        print("SUCCESS:", reading)
        sensor.close()
    except Exception as e:
        print("FAILED:", e)


if __name__ == "__main__":
    print("Testing all three sensors...")
    test_temperature_humidity()
    test_wind()
    test_gps()
    print("\nDone.")
