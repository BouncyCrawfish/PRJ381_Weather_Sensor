"""
GlobalSat BU-353N GPS driver - reads NMEA sentences over USB-serial.

Install:
    pip3 install pyserial pynmea2 --break-system-packages
"""

import serial
import pynmea2

from config import GPS_SERIAL_PORT, GPS_BAUD_RATE, GPS_READ_TIMEOUT_S


class GPSReader:
    def __init__(self, port=GPS_SERIAL_PORT, baudrate=GPS_BAUD_RATE):
        self.serial_conn = serial.Serial(
            port, baudrate=baudrate, timeout=GPS_READ_TIMEOUT_S
        )

    def read(self, max_lines=50):
        """
        Reads lines until it finds a sentence with a valid fix (GGA or RMC),
        or gives up after max_lines. Returns dict with latitude/longitude,
        or None values if no fix was available yet.
        """
        for _ in range(max_lines):
            try:
                line = self.serial_conn.readline().decode("ascii", errors="replace").strip()
            except serial.SerialException:
                break

            if not line.startswith("$"):
                continue

            try:
                msg = pynmea2.parse(line)
            except pynmea2.ParseError:
                continue

            if isinstance(msg, (pynmea2.types.talker.GGA, pynmea2.types.talker.RMC)):
                if getattr(msg, "latitude", None) and getattr(msg, "longitude", None):
                    return {
                        "latitude": round(msg.latitude, 6),
                        "longitude": round(msg.longitude, 6),
                    }

        return {"latitude": None, "longitude": None}

    def close(self):
        self.serial_conn.close()


if __name__ == "__main__":
    gps = GPSReader()
    try:
        print("Waiting for GPS fix (can take up to a minute outdoors)...")
        print(gps.read())
    finally:
        gps.close()
