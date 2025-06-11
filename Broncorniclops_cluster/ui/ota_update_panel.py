from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import subprocess
import threading

class OTAUpdatePanel(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="OTA Update", size_hint=(0.8, 0.5), **kwargs)
        self.status_label = Label(text="Press update to begin", size_hint_y=0.6)

        update_btn = Button(text="Check for Updates", size_hint_y=0.2)
        update_btn.bind(on_press=self.run_update)

        close_btn = Button(text="Close", size_hint_y=0.2)
        close_btn.bind(on_press=self.dismiss)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(self.status_label)
        layout.add_widget(update_btn)
        layout.add_widget(close_btn)

        self.content = layout

    def run_update(self, instance):
        self.status_label.text = "Updating... Please wait."
        threading.Thread(target=self.perform_update).start()

    def perform_update(self):
        try:
            result = subprocess.check_output(["/home/pi/digital_cluster/system/cluster_update.sh"], stderr=subprocess.STDOUT, text=True)
            status = "Update complete." if "updated" in result.lower() or "done" in result.lower() else "Update finished with messages."
        except subprocess.CalledProcessError as e:
            status = "Update failed:\n" + e.output

        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', status), 0)