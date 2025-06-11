
import json
import os

PID_FILE = "data/pid_mappings/pid_config.json"

class PIDManager:
    def __init__(self):
        self.pids = self._load_pids()

    def _load_pids(self):
        if os.path.exists(PID_FILE):
            with open(PID_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_pids(self):
        with open(PID_FILE, 'w') as f:
            json.dump(self.pids, f, indent=2)

    def get_label(self, pid):
        return self.pids.get(pid, {}).get("label", f"PID {pid}")

    def set_label(self, pid, label):
        if pid not in self.pids:
            self.pids[pid] = {}
        self.pids[pid]["label"] = label
        self.save_pids()

    def register_pid(self, pid, label="Unknown PID"):
        if pid not in self.pids:
            self.pids[pid] = {"label": label}
            self.save_pids()

    def all_pids(self):
        return self.pids
