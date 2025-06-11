import os
import json
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

PROFILE_DIR = "/home/pi/digital_cluster/layouts/profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)

class GaugeProfileSwitcher(Popup):
    def __init__(self, layout_manager, **kwargs):
        super().__init__(title="Gauge Profile Switcher", size_hint=(0.8, 0.6), **kwargs)
        self.layout_manager = layout_manager
        self.profiles = self.scan_profiles()

        self.spinner = Spinner(text="Select Profile", values=sorted(self.profiles.keys()), size_hint_y=0.2)

        btn_load = Button(text="Apply Profile", size_hint_y=0.2)
        btn_load.bind(on_press=self.apply_profile)

        btn_close = Button(text="Close", size_hint_y=0.2)
        btn_close.bind(on_press=self.dismiss)

        self.status_label = Label(text="", size_hint_y=0.2)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(self.spinner)
        layout.add_widget(btn_load)
        layout.add_widget(self.status_label)
        layout.add_widget(btn_close)

        self.content = layout

    def scan_profiles(self):
        profiles = {}
        for fname in os.listdir(PROFILE_DIR):
            if fname.endswith(".json"):
                path = os.path.join(PROFILE_DIR, fname)
                try:
                    with open(path) as f:
                        profiles[fname] = json.load(f)
                except:
                    pass
        return profiles

    def apply_profile(self, *args):
        selected = self.spinner.text
        if selected in self.profiles:
            self.layout_manager.apply_layout_data(self.profiles[selected])
            self.status_label.text = f"Profile '{selected}' applied."
        else:
            self.status_label.text = "No profile selected."