import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from log_manager import LogManager

class LogSettingsPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.log_mgr = LogManager()

        self.status = Label(text="Logging is ON" if self.log_mgr.is_enabled() else "Logging is OFF")
        self.add_widget(self.status)

        toggle_btn = ToggleButton(text="Enable Logging" if not self.log_mgr.is_enabled() else "Disable Logging", size_hint=(1, 0.2))
        toggle_btn.bind(on_press=self.toggle_logging)
        self.add_widget(toggle_btn)

        self.add_widget(Label(text="Delete logs by source:"))
        self.source_spinner = Spinner(values=self.get_sources(), size_hint=(1, 0.2))
        self.add_widget(self.source_spinner)

        delete_btn = Button(text="Delete Logs", size_hint=(1, 0.2))
        delete_btn.bind(on_press=self.delete_logs)
        self.add_widget(delete_btn)

        cleanup_btn = Button(text="Clean Logs >30 Days", size_hint=(1, 0.2))
        cleanup_btn.bind(on_press=lambda x: self.clean_old_logs())
        self.add_widget(cleanup_btn)

    def toggle_logging(self, instance):
        new_state = not self.log_mgr.is_enabled()
        self.log_mgr.toggle_logging(new_state)
        self.status.text = "Logging is ON" if new_state else "Logging is OFF"
        instance.text = "Disable Logging" if new_state else "Enable Logging"

    def get_sources(self):
        sources = set()
        for fname in os.listdir(self.log_mgr.LOG_DIR):
            if "_" in fname:
                sources.add(fname.split("_")[0])
        return sorted(sources)

    def delete_logs(self, instance):
        source = self.source_spinner.text
        if source:
            self.log_mgr.delete_logs_by_source(source)
            self.source_spinner.values = self.get_sources()

    def clean_old_logs(self):
        self.log_mgr.auto_cleanup()