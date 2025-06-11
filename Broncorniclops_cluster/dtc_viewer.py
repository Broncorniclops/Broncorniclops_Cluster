from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
import datetime
import os

LOG_FILE = "data/logs/dtc_expand_log.txt"

class DTCViewer(BoxLayout):
    def __init__(self, dtc_data, can_data=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.dtc_data = dtc_data
        self.can_data = can_data or {}
        self.labels = []

        self.scroll = ScrollView(size_hint=(1, 0.9))
        self.grid = GridLayout(cols=1, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)

        self.add_widget(self.scroll)

        self.clear_button = Button(text="Clear DTCs", size_hint=(1, 0.1))
        self.clear_button.bind(on_press=self.clear_dtcs)
        self.add_widget(self.clear_button)

        self.refresh()

    def refresh(self):
        self.grid.clear_widgets()
        self.labels.clear()

        if not self.dtc_data:
            label = Label(text="No Diagnostic Trouble Codes")
            self.grid.add_widget(label)
            self.labels.append(label)
        else:
            for code, description in self.dtc_data.items():
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
                icon = Image(source='assets/icons/warning.png', size_hint=(None, None), size=(32, 32))
                label = Button(text=f"{code}: {description}", halign="left")
                label.bind(on_press=lambda instance, c=code, d=description: self.expand_dtc(c, d))
                row.add_widget(icon)
                row.add_widget(label)
                self.grid.add_widget(row)
                self.labels.append(row)

    def clear_dtcs(self, instance):
        self.dtc_data.clear()
        self.refresh()

    def expand_dtc(self, code, description):
        # Log the viewed DTC and CAN snapshot
        timestamp = datetime.datetime.now().isoformat()
        os.makedirs("data/logs", exist_ok=True)
        with open(LOG_FILE, "a") as log:
            log.write(f"---\n{timestamp} – Viewed {code}: {description}\n")
            log.write("Sensor Snapshot:\n")
            for key, val in self.can_data.items():
                log.write(f"{key}: {val}\n")
            log.write("---\n")

        # Create and auto-dismiss popup
        popup = Popup(
            title=f"{code} Detail",
            content=Label(text=f"Code: {code}\nDescription: {description}\nDetails coming soon..."),
            size_hint=(0.7, 0.5),
            auto_dismiss=True
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 10)