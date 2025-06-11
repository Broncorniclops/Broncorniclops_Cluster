import subprocess
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from theme_manager import ThemeManager
from visual_theme_builder import VisualThemeBuilder
from gesture_binding_editor import GestureBindingEditor
from touchscreen_calibrator import TouchscreenCalibrator
from export_config_to_usb import ConfigExporter
from gauge_profile_switcher import GaugeProfileSwitcher
from log_viewer import LogViewer
from can_log_viewer import CANLogViewer
from ota_update_panel import OTAUpdatePanel
from can_pid_debugger import CANPIDDebugger
from pid_debugger_launcher import PIDDebuggerLauncher

class SettingsPopup(Popup):
    def __init__(self, app=None, **kwargs):
        super().__init__(title="Settings", size_hint=(0.9, 0.95), **kwargs)
        self.app = app
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        layout.add_widget(Button(text="Theme Manager", on_press=self.open_theme_manager))
        layout.add_widget(Button(text="Theme Builder", on_press=self.open_theme_builder))
        layout.add_widget(Button(text="Gesture Binding Editor", on_press=self.open_gesture_editor))
        layout.add_widget(Button(text="Touchscreen Calibration", on_press=self.open_touch_calibration))
        layout.add_widget(Button(text="Export Config to USB", on_press=self.export_config))
        layout.add_widget(Button(text="Gauge Profile Switcher", on_press=self.open_profile_switcher))
        layout.add_widget(Button(text="Log V\n        layout.add_widget(PIDDebuggerLauncher())iewer", on_press=self.open_log_viewer))
        layout.add_widget(Button(text="CAN Log Viewer", on_press=self.open_can_log_viewer))
        layout.add_widget(Button(text="OTA Update Panel", on_press=self.open_ota_update))
        layout.add_widget(Button(text="CAN PID Debugger", on_press=self.open_can_pid_debugger))
        layout.add_widget(Button(text="Manual Shutdown", on_press=self.trigger_manual_shutdown))

        close_btn = Button(text="Close", size_hint_y=0.15)
        close_btn.bind(on_press=self.dismiss)
        layout.add_widget(close_btn)

        self.content = layout

    def open_theme_manager(self, *args):
        ThemeManager(apply_callback=lambda x: None).open()

    def open_theme_builder(self, *args):
        VisualThemeBuilder().open()

    def open_gesture_editor(self, *args):
        GestureBindingEditor().open()

    def open_touch_calibration(self, *args):
        TouchscreenCalibrator().open()

    def export_config(self, *args):
        exporter = ConfigExporter()
        result = exporter.export_all()
        self.show_status_popup(result)

    def open_profile_switcher(self, *args):
        GaugeProfileSwitcher(self.app.layout_manager if self.app else None).open()

    def open_log_viewer(self, *args):
        LogViewer().open()

    def open_can_log_viewer(self, *args):
        CANLogViewer().open()

    def open_ota_update(self, *args):
        OTAUpdatePanel().open()

    def open_can_pid_debugger(self, *args):
        CANPIDDebugger().open()

    def show_status_popup(self, message):
        popup = Popup(title="Status", content=Label(text=message),
                      size_hint=(0.6, 0.3))
        popup.open()

    def trigger_manual_shutdown(self, *args):
        popup = Popup(title="Shutting Down", content=Label(text="System will shut down..."),
                      size_hint=(0.6, 0.3))
        popup.open()
        subprocess.call(['sudo', 'shutdown', '-h', 'now'])