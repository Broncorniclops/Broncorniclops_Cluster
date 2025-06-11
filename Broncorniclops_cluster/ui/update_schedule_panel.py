import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button

SCHEDULE_FILE = "/home/pi/.cluster_update_schedule"

class UpdateSchedulePanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.add_widget(Label(text="Auto Update Schedule:"))

        self.spinner = Spinner(
            text='manual',
            values=('manual', 'daily', 'weekly'),
            size_hint=(1, 0.2)
        )
        self.spinner.bind(text=self.set_schedule)
        self.add_widget(self.spinner)

        self.status = Label(text="", size_hint=(1, 0.3))
        self.add_widget(self.status)

        self.load_schedule()

    def load_schedule(self):
        if os.path.exists(SCHEDULE_FILE):
            with open(SCHEDULE_FILE, "r") as f:
                saved = f.read().strip()
                if saved in self.spinner.values:
                    self.spinner.text = saved
                    self.status.text = f"Loaded: {saved}"

    def set_schedule(self, spinner, value):
        with open(SCHEDULE_FILE, "w") as f:
            f.write(value)
        self.status.text = f"Schedule set to: {value}"
        # Here you would update crontab or a service timer