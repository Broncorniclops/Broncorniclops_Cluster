from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock

LOG_PATH = "/home/pi/digital_cluster/logs/can.log"

class CANLogViewer(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="CAN Log Viewer", size_hint=(0.95, 0.95), **kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.search_input = TextInput(hint_text="Filter by ID or PID...", multiline=False, size_hint_y=0.1)
        self.search_input.bind(on_text_validate=self.update_display)
        layout.add_widget(self.search_input)

        self.log_output = TextInput(readonly=True, font_size=12, size_hint_y=0.8)
        layout.add_widget(self.log_output)

        close_btn = Button(text="Close", size_hint_y=0.1)
        close_btn.bind(on_press=self.dismiss)
        layout.add_widget(close_btn)

        self.content = layout
        Clock.schedule_once(lambda dt: self.update_display(), 0.1)

    def update_display(self, *args):
        filter_text = self.search_input.text.lower()
        try:
            with open(LOG_PATH, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            self.log_output.text = "CAN log not found."
            return

        if filter_text:
            filtered = [line for line in lines if filter_text in line.lower()]
        else:
            filtered = lines

        self.log_output.text = "".join(filtered[-500:])