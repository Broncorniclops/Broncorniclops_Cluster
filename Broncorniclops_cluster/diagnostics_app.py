from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from fan_controller import FanController
from ambient_temp_sensor import AmbientTempSensor
from diagnostics_overlay import DiagnosticsOverlay

class RootLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ambient_sensor = AmbientTempSensor(pin=4)
        self.fan_controller = FanController(gpio_pwm_cpu=18, gpio_pwm_ambient=13, ambient_sensor=self.ambient_sensor)

        self.overlay = DiagnosticsOverlay(self.fan_controller, self.ambient_sensor)
        self.overlay.size_hint = (0.3, 0.3)
        self.overlay.pos_hint = {'right': 1, 'top': 1}
        self.overlay_visible = False
        self.add_widget(self.overlay)
        self.overlay.opacity = 0  # Start hidden

        Clock.schedule_interval(self.update_overlay, 5)
        self.register_event_type("on_two_finger_swipe")

    def update_overlay(self, dt):
        if self.overlay_visible:
            self.overlay.update()

    def on_touch_down(self, touch):
        if len(self._touches) == 1:
            self._touches = [touch]
        elif len(self._touches) == 0:
            self._touches.append(touch)
        elif len(self._touches) == 1 and self._touches[0] is not touch:
            self._touches.append(touch)
            self.dispatch("on_two_finger_swipe")
        return super().on_touch_down(touch)

    def on_two_finger_swipe(self, *args):
        self.toggle_overlay()

    def toggle_overlay(self):
        self.overlay_visible = not self.overlay_visible
        self.overlay.opacity = 1 if self.overlay_visible else 0

class DiagnosticsApp(App):
    def build(self):
        root = RootLayout()
        root._touches = []
        return root

if __name__ == "__main__":
    DiagnosticsApp().run()