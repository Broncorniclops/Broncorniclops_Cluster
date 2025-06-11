import os
import time
from datetime import datetime, timedelta

LOG_DIR = "/home/pi/digital_cluster/logs"
LOG_ENABLED_FILE = "/home/pi/digital_cluster/.log_enabled"

class LogManager:
    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        self.enabled = os.path.exists(LOG_ENABLED_FILE)

    def toggle_logging(self, state: bool):
        self.enabled = state
        if state:
            open(LOG_ENABLED_FILE, "a").close()
        else:
            if os.path.exists(LOG_ENABLED_FILE):
                os.remove(LOG_ENABLED_FILE)

    def is_enabled(self):
        return self.enabled

    def write_log(self, source: str, message: str):
        if not self.enabled:
            return
        filename = f"{source}_{datetime.now().strftime('%Y-%m-%d')}.log"
        path = os.path.join(LOG_DIR, filename)
        timestamp = datetime.now().strftime('%H:%M:%S')
        with open(path, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def delete_logs_by_source(self, source: str):
        for f in os.listdir(LOG_DIR):
            if f.startswith(source + "_"):
                os.remove(os.path.join(LOG_DIR, f))

    def auto_cleanup(self, max_age_days=30):
        now = time.time()
        for f in os.listdir(LOG_DIR):
            path = os.path.join(LOG_DIR, f)
            if os.path.isfile(path):
                age_days = (now - os.path.getmtime(path)) / 86400
                if age_days > max_age_days:
                    os.remove(path)