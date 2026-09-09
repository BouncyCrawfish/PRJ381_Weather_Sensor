"""
Checks whether the GPS module is producing valid latitude/longitude
readings, using the project's own GPSReader driver (sensors/gps_reader.py).

Run from inside the iwos_weather_station folder:
    python3 check_gps.py

Stop with Ctrl+C.
"""

import time

from sensors.gps_reader import GPSReader


def main():
    print("Opening GPS... take this outdoors with a clear view of the sky "
          "for best results. Ctrl+C to stop.\n")

    gps = GPSReader()
    attempt = 0

    try:
        while True:
            attempt += 1
            reading = gps.read()
            lat = reading.get("latitude")
            lon = reading.get("longitude")

            if lat is not None and lon is not None:
                print(f"[{attempt}] FIX -> latitude={lat}, longitude={lon}")
            else:
                print(f"[{attempt}] No fix yet (latitude/longitude are None). "
                      "Still listening...")

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        gps.close()


if __name__ == "__main__":
    main()