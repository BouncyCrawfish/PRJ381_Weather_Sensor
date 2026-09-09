"""
Local CSV logger - keeps a backup of every reading on the Pi's SD card,
in case connectivity to the cloud drops mid-race.
"""

import csv
import os

from config import CSV_LOG_PATH


class DataLogger:
    def __init__(self, path=CSV_LOG_PATH):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._ensure_header(path=self.path)

    def _ensure_header(self, path):
        file_exists = os.path.isfile(path)
        if not file_exists:
            with open(path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "temperature_c", "humidity_pct",
                    "pressure_hpa", "altitude_m",
                    "wind_speed_ms", "latitude", "longitude",
                ])

    def log(self, reading: dict):
        """Appends one reading (dict) as a row."""
        with open(self.path, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                reading.get("timestamp"),
                reading.get("temperature_c"),
                reading.get("humidity_pct"),
                reading.get("pressure_hpa"),
                reading.get("altitude_m"),
                reading.get("wind_speed_ms"),
                reading.get("latitude"),
                reading.get("longitude"),
            ])