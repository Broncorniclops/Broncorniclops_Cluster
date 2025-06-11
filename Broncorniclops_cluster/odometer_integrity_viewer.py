from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from datetime import datetime
import os

LOG_PATH = "/home/pi/digital_cluster/logs/odometer_integrity.log"

class OdometerIntegrityViewer(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="Odometer Integrity Log", size_hint=(0.95, 0.9), **kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.output = TextInput(readonly=True, font_size='12sp')

        self.refresh_log()

        close_btn = Button(text="Close", size_hint_y=0.1)
        close_btn.bind(on_press=self.dismiss)

        layout.add_widget(self.output)
        layout.add_widget(close_btn)

        self.content = layout

    def refresh_log(self):
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                self.output.text = f.read()
        else:
            self.output.text = "[No odometer integrity log found]"