import os
import json
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

THEME_DIR = "/home/pi/digital_cluster/themes"

class VisualThemeBuilder(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="Theme Builder", size_hint=(0.95, 0.95), **kwargs)
        self.colors = {
            "background": [0, 0, 0, 1],
            "foreground": [1, 1, 1, 1],
            "accent": [1, 0, 0, 1]
        }

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.color_pickers = {}
        for key in self.colors:
            cp = ColorPicker(size_hint_y=0.6)
            cp.bind(color=self.on_color_change(key))
            layout.add_widget(Button(text=f"{key.capitalize()} Color", size_hint_y=0.1, disabled=True))
            layout.add_widget(cp)
            self.color_pickers[key] = cp

        self.filename_input = TextInput(hint_text="Theme name (without extension)", multiline=False, size_hint_y=0.1)
        layout.add_widget(self.filename_input)

        save_btn = Button(text="Save Theme", size_hint_y=0.1)
        save_btn.bind(on_press=self.save_theme)
        layout.add_widget(save_btn)

        close_btn = Button(text="Close", size_hint_y=0.1)
        close_btn.bind(on_press=self.dismiss)
        layout.add_widget(close_btn)

        self.content = layout

    def on_color_change(self, key):
        def update_color(instance, value):
            self.colors[key] = value
        return update_color

    def save_theme(self, *args):
        theme_name = self.filename_input.text.strip()
        if not theme_name:
            return
        os.makedirs(THEME_DIR, exist_ok=True)
        with open(os.path.join(THEME_DIR, f"{theme_name}.json"), "w") as f:
            json.dump(self.colors, f, indent=2)