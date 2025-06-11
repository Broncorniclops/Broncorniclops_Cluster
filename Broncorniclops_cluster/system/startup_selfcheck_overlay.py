from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import os
from datetime import datetime

LOG_PATH = "/home/pi/digital_cluster/logs/selfcheck.log"

class SelfCheckOverlay(Popup):
    def __init__(self, failures, **kwargs):
        super().__init__(title="System Diagnostics", size_hint=(0.9, 0.9), **kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        if failures:
            for item in failures:
                layout.add_widget(Label(text=f"[FAILED] {item}", color=(1, 0, 0, 1)))
            self.log_failures(failures)
        else:
            layout.add_widget(Label(text="All systems OK", color=(0, 1, 0, 1)))
        self.content = layout

    def log_failures(self, items):
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a") as f:
            f.write(f"[{datetime.now()}] Boot Check Failures:\n")
            for i in items:
                f.write(f"  - {i}\n")