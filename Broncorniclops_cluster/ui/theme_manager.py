import os
import json
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

THEME_DIR = "/home/pi/digital_cluster/themes"

class ThemeManager(Popup):
    def __init__(self, apply_callback, **kwargs):
        super().__init__(title="Theme Manager", size_hint=(0.85, 0.6), **kwargs)
        self.apply_callback = apply_callback
        self.themes = self.scan_themes()

        self.spinner = Spinner(text="Select Theme", values=sorted(self.themes.keys()), size_hint_y=0.2)
        self.spinner.bind(text=self.preview_theme)

        self.preview_label = Label(text="Theme preview will appear here", size_hint_y=0.5)

        btn_apply = Button(text="Apply Theme", size_hint_y=0.15)
        btn_apply.bind(on_press=self.apply_selected)

        btn_close = Button(text="Close", size_hint_y=0.15)
        btn_close.bind(on_press=self.dismiss)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(self.spinner)
        layout.add_widget(self.preview_label)
        layout.add_widget(btn_apply)
        layout.add_widget(btn_close)

        self.content = layout

    def scan_themes(self):
        themes = {}
        if os.path.exists(THEME_DIR):
            for f in os.listdir(THEME_DIR):
                if f.endswith(".json"):
                    path = os.path.join(THEME_DIR, f)
                    try:
                        with open(path) as jf:
                            themes[f] = json.load(jf)
                    except:
                        pass
        return themes

    def preview_theme(self, spinner, value):
        theme = self.themes.get(value, {})
        self.preview_label.text = json.dumps(theme, indent=2)

    def apply_selected(self, *args):
        selected = self.spinner.text
        if selected in self.themes:
            self.apply_callback(self.themes[selected])
        self.dismiss()