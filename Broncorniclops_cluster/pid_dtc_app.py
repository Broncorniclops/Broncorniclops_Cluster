from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from pid_manager import PIDManager
from dtc_viewer import DTCViewer

class MainPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.pid_manager = PIDManager()
        # Example DTCs - replace with actual CAN readout
        self.dtc_data = {
            "P0133": "O2 Sensor Slow Response",
            "P0420": "Catalyst System Efficiency Below Threshold"
        }

        self.dtc_viewer = DTCViewer(self.dtc_data)
        self.add_widget(self.dtc_viewer)

        self.load_pids_button = Button(text="Print All PIDs")
        self.load_pids_button.bind(on_press=self.show_pids)
        self.add_widget(self.load_pids_button)

    def show_pids(self, instance):
        for pid, info in self.pid_manager.all_pids().items():
            print(f"{pid}: {info}")

class PIDApp(App):
    def build(self):
        return MainPanel()

if __name__ == "__main__":
    PIDApp().run()