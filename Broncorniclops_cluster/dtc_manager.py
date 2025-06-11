import json
import os

DTC_LOG_FILE = "data/logs/dtc_snapshot.json"

class DTCManager:
    def __init__(self, can_data):
        self.can_data = can_data
        self.dtc_data = self._load_dtcs()

    def _load_dtcs(self):
        if os.path.exists(DTC_LOG_FILE):
            with open(DTC_LOG_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_dtcs(self):
        with open(DTC_LOG_FILE, 'w') as f:
            json.dump(self.dtc_data, f, indent=2)

    def update_from_can(self):
        dtcs = self.can_data.get("DTC_CODES", [])
        for code in dtcs:
            if code not in self.dtc_data:
                self.dtc_data[code] = "Unknown Fault"
        self.save_dtcs()

    def clear_dtcs(self):
        self.dtc_data.clear()
        self.save_dtcs()

    def get_dtcs(self):
        return self.dtc_data