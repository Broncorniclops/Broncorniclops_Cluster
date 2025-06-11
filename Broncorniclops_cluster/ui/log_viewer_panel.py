from usb_exporter import export_logs_to_usb
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.textinput import TextInput
from datetime import datetime

LOG_DIR = "/home/pi/digital_cluster/logs"
EXPORT_DIR = "/home/pi/digital_cluster/exported_logs"

class LogViewerPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.label = Label(text="Select a log to view", size_hint_y=0.1)
        self.add_widget(self.label)

        self.log_spinner = Spinner(values=self.list_logs(), size_hint_y=0.1)
        self.log_spinner.bind(text=self.load_log)
        self.add_widget(self.log_spinner)

        self.filter_input = TextInput(hint_text="Filter by keyword (press Enter)", multiline=False, size_hint_y=0.1)
        self.filter_input.bind(on_text_validate=self.apply_filter)
        self.add_widget(self.filter_input)

        self.viewer = TextInput(readonly=True, font_size='12sp', size_hint_y=0.6)
        self.scroll = ScrollView(size_hint=(1, 0.6))
        self.scroll.add_widget(self.viewer)
        self.add_widget(self.scroll)

        controls = BoxLayout(size_hint_y=0.1, spacing=10)
        export_btn = Button(text="Export")
        usb_btn = Button(text="Export to USB")
        export_btn.bind(on_press=self.export_log)
        refresh_btn = Button(text="Refresh List")
        refresh_btn.bind(on_press=lambda x: self.refresh())
        controls.add_widget(export_btn)
        usb_btn.bind(on_press=self.export_to_usb)
        controls.add_widget(usb_btn)
        controls.add_widget(refresh_btn)
        self.add_widget(controls)

        self.raw_log = ""
        os.makedirs(EXPORT_DIR, exist_ok=True)

    def list_logs(self):
        if not os.path.exists(LOG_DIR):
            return []
        return sorted([f for f in os.listdir(LOG_DIR) if f.endswith(".log")])

    def load_log(self, spinner, filename):
        try:
            path = os.path.join(LOG_DIR, filename)
            with open(path) as f:
                self.raw_log = f.read()
            self.viewer.text = self.raw_log
        except Exception as e:
            self.viewer.text = f"Error loading log: {e}"

    def apply_filter(self, instance):
        keyword = self.filter_input.text.strip()
        if keyword and self.raw_log:
            lines = self.raw_log.splitlines()
            filtered = [line for line in lines if keyword in line]
            self.viewer.text = "\n".join(filtered)
        else:
            self.viewer.text = self.raw_log

    def export_log(self, instance):
        if not self.raw_log:
            return
        filename = self.log_spinner.text.replace(".log", "") + "_exported_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
        path = os.path.join(EXPORT_DIR, filename)
        with open(path, "w") as f:
            f.write(self.viewer.text)

    def export_to_usb(self, instance):
        result = export_logs_to_usb()
        self.viewer.text = result