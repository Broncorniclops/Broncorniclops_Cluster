from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import json
import os

SETTINGS_FILE = "data/system/odometer_protection.json"

class OdometerSettingsPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="Odometer Protection", size_hint=(0.8, 0.5), **kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False)
        self.layout.add_widget(Label(text="Set/Edit credentials for odometer change protection:"))
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)

        self.save_button = Button(text="Save")
        self.save_button.bind(on_press=self.save_settings)
        self.layout.add_widget(self.save_button)

        self.load_existing()
        self.content = self.layout

    def load_existing(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                self.username_input.text = data.get("username", "")
                self.password_input.text = data.get("password", "")

    def save_settings(self, instance):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({
                "username": self.username_input.text,
                "password": self.password_input.text
            }, f, indent=2)
        self.dismiss()