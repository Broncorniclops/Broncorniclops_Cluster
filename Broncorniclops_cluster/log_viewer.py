from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import os

class LogViewer(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="Log Viewer", size_hint=(0.95, 0.95), **kwargs)
        panel = TabbedPanel(do_default_tab=False)

        self.tabs = {
            "General": "/home/pi/digital_cluster/logs/general.log",
            "CAN": "/home/pi/digital_cluster/logs/can.log",
            "SelfCheck": "/home/pi/digital_cluster/logs/selfcheck.log",
            "Odometer": "/home/pi/digital_cluster/logs/odometer_integrity.log"
        }

        for name, path in self.tabs.items():
            tab = TabbedPanelItem(text=name)
            tab_content = BoxLayout()
            output = TextInput(readonly=True, font_size=12)
            tab_content.add_widget(output)
            tab.add_widget(tab_content)
            panel.add_widget(tab)
            self.load_log(output, path)

        self.content = panel

    def load_log(self, widget, path):
        try:
            with open(path) as f:
                widget.text = f.read()
        except:
            widget.text = "[Log file not found]"