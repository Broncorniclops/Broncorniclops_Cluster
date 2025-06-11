import json
import os
from datetime import datetime

SETTINGS_FILE = "data/system/odometer_protection.json"
LOG_FILE = "logs/odometer_changes.log"
ODO_FILE = "data/system/odometer.json"

class OdometerManager:
    def __init__(self):
        os.makedirs(os.path.dirname(ODO_FILE), exist_ok=True)
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        self.odo = 0.0
        self.trip = 0.0
        self.load()

    def load(self):
        if os.path.exists(ODO_FILE):
            with open(ODO_FILE, "r") as f:
                data = json.load(f)
                self.odo = data.get("odo", 0.0)
                self.trip = data.get("trip", 0.0)

    def save(self):
        with open(ODO_FILE, "w") as f:
            json.dump({"odo": self.odo, "trip": self.trip}, f, indent=2)

    def reset_trip(self):
        self.trip = 0.0
        self.save()

    def add_distance(self, miles):
        self.odo += miles
        self.trip += miles
        self.save()

    def verify_password(self, username, password):
        return username == "admin" and password == "cluster"

    def log_change(self, reason="manual override"):
        with open(LOG_FILE, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"[{timestamp}] Odometer changed: {self.odo:.1f} mi - Reason: {reason}\n"
            f.write(entry)