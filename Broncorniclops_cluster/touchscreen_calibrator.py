from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.widget import Widget

class TouchscreenCalibrator(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="Touchscreen Calibration", size_hint=(1, 1), auto_dismiss=False, **kwargs)
        self.points = []
        self.instructions = [
            "Touch the TOP LEFT corner",
            "Touch the TOP RIGHT corner",
            "Touch the BOTTOM RIGHT corner",
            "Touch the BOTTOM LEFT corner"
        ]
        self.index = 0

        self.label = Label(text=self.instructions[0], font_size='20sp', size_hint=(1, 0.1))

        self.touch_area = Widget()
        self.touch_area.bind(on_touch_down=self.record_touch)

        self.done_btn = Button(text="Finish", size_hint=(1, 0.1))
        self.done_btn.bind(on_press=self.dismiss)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(self.touch_area)
        layout.add_widget(self.done_btn)

        self.content = layout

    def record_touch(self, widget, touch):
        self.points.append((touch.x, touch.y))
        self.index += 1
        if self.index < len(self.instructions):
            self.label.text = self.instructions[self.index]
        else:
            self.label.text = "Calibration complete"
            print("Calibration points:", self.points)