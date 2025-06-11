import subprocess
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class AutoUpdatePanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.status = Label(text="Tap to check for updates.")
        self.add_widget(self.status)

        update_btn = Button(text="Run Update", size_hint=(1, 0.3))
        update_btn.bind(on_press=self.run_update)
        self.add_widget(update_btn)

    def run_update(self, instance):
        try:
            subprocess.run(["/bin/bash", "/home/pi/update_cluster.sh"], check=True)
            self.status.text = "Update complete."
        except subprocess.CalledProcessError:
            self.status.text = "Update failed."