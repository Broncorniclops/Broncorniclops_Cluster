from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
import json
import os

BINDINGS_PATH = "/home/pi/digital_cluster/config/gesture_bindings.json"

DEFAULT_ACTIONS = [
    "Toggle Diagnostic Overlay",
    "Switch Screen Left",
    "Switch Screen Right",
    "Toggle Night Mode",
    "Reset Trip",
    "Open CAN Log Viewer",
    "Open Settings Panel"
]

DEFAULT_GESTURES = [
    "Two-Finger Swipe Down",
    "Two-Finger Swipe Left",
    "Two-Finger Swipe Right",
    "Long Press",
    "Double Tap",
    "Three-Finger Tap"
]

class GestureBindingEditor(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="Gesture Binding Editor", size_hint=(0.9, 0.9), **kwargs)
        self.bindings = self.load_bindings()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.pairs = []
        for gesture in DEFAULT_GESTURES:
            row = BoxLayout(size_hint_y=None, height=40)
            label = Button(text=gesture, size_hint_x=0.5, disabled=True)
            spinner = Spinner(text=self.bindings.get(gesture, "None"), values=DEFAULT_ACTIONS, size_hint_x=0.5)
            row.add_widget(label)
            row.add_widget(spinner)
            layout.add_widget(row)
            self.pairs.append((gesture, spinner))

        btn_save = Button(text="Save", size_hint_y=0.1)
        btn_save.bind(on_press=self.save_bindings)

        btn_close = Button(text="Close", size_hint_y=0.1)
        btn_close.bind(on_press=self.dismiss)

        layout.add_widget(btn_save)
        layout.add_widget(btn_close)

        self.content = layout

    def load_bindings(self):
        if os.path.exists(BINDINGS_PATH):
            with open(BINDINGS_PATH) as f:
                return json.load(f)
        return {}

    def save_bindings(self, *args):
        new_bindings = {gesture: spinner.text for gesture, spinner in self.pairs}
        os.makedirs(os.path.dirname(BINDINGS_PATH), exist_ok=True)
        with open(BINDINGS_PATH, "w") as f:
            json.dump(new_bindings, f, indent=2)