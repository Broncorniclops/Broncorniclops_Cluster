from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock

from settings_popup import SettingsPopup
from startup_selfcheck_overlay import StartupSelfCheckOverlay
from layout_manager import LayoutManager
from sensor_manager import SensorManager
from theme_loader import ThemeLoader
from fan_controller import FanController

class ClusterApp(App):
    def build(self):
        self.layout_manager = LayoutManager()
        self.sensor_manager = SensorManager()
        self.fan_controller = FanController()
        self.theme_loader = ThemeLoader()

        self.root_layout = BoxLayout(orientation='vertical')

        self.settings_button = Button(text="Settings", size_hint_y=0.1)
        self.settings_button.bind(on_press=self.open_settings)
        self.root_layout.add_widget(self.settings_button)

        self.root_layout.add_widget(self.layout_manager)

        # Schedule periodic updates
        Clock.schedule_interval(self.update_sensors, 1/10.0)
        Clock.schedule_interval(self.fan_controller.update, 1.0)

        # Check for issues at boot
        Clock.schedule_once(self.run_selfcheck, 1)

        return self.root_layout

    def run_selfcheck(self, *args):
        issues = []
        if not self.sensor_manager.can_ready():
            issues.append("CAN interface not detected")
        if not self.fan_controller.pwm_initialized:
            issues.append("Fan PWM controller not initialized")
        if issues:
            overlay = StartupSelfCheckOverlay(issues)
            overlay.open()

    def update_sensors(self, dt):
        self.sensor_manager.update()
        self.layout_manager.update_gauges(self.sensor_manager.get_all_data())

    def open_settings(self, instance):
        SettingsPopup(app=self).open()

if __name__ == "__main__":
    ClusterApp().run()