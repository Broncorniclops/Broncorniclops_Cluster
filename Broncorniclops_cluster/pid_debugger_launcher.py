
import subprocess
import os
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

class PIDDebuggerLauncher(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.launch_button = Button(text='Launch PID Debugger UI', size_hint_y=None, height=50)
        self.launch_button.bind(on_release=self.launch_debugger)
        self.add_widget(self.launch_button)

    def is_already_running(self):
        try:
            output = subprocess.check_output(["pgrep", "-f", "pid_combined_tool.py"]).decode().strip()
            return bool(output)
        except subprocess.CalledProcessError:
            return False

    def bring_to_foreground(self):
        try:
            # Try to bring any matching window forward using wmctrl
            subprocess.call(["wmctrl", "-a", "Digital Cluster: PID Debugger UI"])
        except Exception as e:
            print("Foreground error:", e)

    def launch_debugger(self, instance):
        if self.is_already_running():
            self.bring_to_foreground()
            popup = Popup(title="Already Running",
                          content=Button(text="PID Debugger is already running. Focused window."),
                          size_hint=(0.6, 0.3))
            popup.open()
            return

        try:
            subprocess.Popen(["/usr/bin/python3", "/home/pi/digital_cluster/tools/pid_combined_tool.py"])
        except Exception as e:
            error_popup = Popup(title="Launch Error", content=Button(text=str(e)), size_hint=(0.7, 0.3))
            error_popup.open()
