from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import os

class StartupSelfCheck:
    def __init__(self, root_widget, check_results_callback=None):
        self.root = root_widget
        self.check_results_callback = check_results_callback
        self.failures = []

    def run_checks(self):
        self.failures.clear()

        if not os.path.exists("/dev/i2c-1"):
            self.failures.append("I2C Bus Not Found")

        if not self.check_can0():
            self.failures.append("CAN Interface (can0) not ready")

        if not os.path.exists("/tmp/ups_notify.sock"):
            self.failures.append("UPS Notify Socket Missing")

        if not self.check_pwm():
            self.failures.append("Fan PWM Control Error")

        if self.failures:
            Clock.schedule_once(self.show_trigger_popup, 1.0)

        if self.check_results_callback:
            self.check_results_callback(self.failures)

    def check_can0(self):
        try:
            with open("/sys/class/net/can0/operstate", "r") as f:
                return f.read().strip() == "up"
        except:
            return False

    def check_pwm(self):
        return os.path.exists("/sys/class/pwm") or os.path.exists("/dev/gpiochip0")

    def show_trigger_popup(self, dt):
        btn = Button(text="View System Diagnostics", size_hint=(0.5, 0.15), pos_hint={'center_x':0.5, 'center_y':0.5})
        popup = Popup(title="Startup Check Warning", content=btn, size_hint=(0.7, 0.3))
        btn.bind(on_press=lambda x: self.open_overlay(popup))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 10)

    def open_overlay(self, popup):
        popup.dismiss()
        from startup_selfcheck_overlay import SelfCheckOverlay
        overlay = SelfCheckOverlay(self.failures)
        overlay.open()