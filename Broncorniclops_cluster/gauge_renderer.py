from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Rectangle, Ellipse, RoundedRectangle, InstructionGroup
from math import radians, cos, sin

class GaugeRenderer(Widget):
    def __init__(self, gauge_type='digital', min_val=0, max_val=100, value=0, units='', **kwargs):
        super().__init__(**kwargs)
        self.gauge_type = gauge_type
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.units = units
        self.label = Label(text='', font_size=20, size_hint=(1, 1), pos=self.pos)
        self.add_widget(self.label)
        self.bind(pos=self.update, size=self.update)

    def set_value(self, new_value):
        self.value = new_value
        self.update()

    def update(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self.gauge_type == 'bar':
                self._draw_bar_3d()
            elif self.gauge_type == 'needle':
                self._draw_needle_3d()
            else:
                self._draw_digital()

    def _draw_bar_3d(self):
        pct = (self.value - self.min_val) / (self.max_val - self.min_val)
        pct = max(0, min(1, pct))

        # Background with shadow
        Color(0.1, 0.1, 0.1)
        RoundedRectangle(pos=self.pos, size=self.size, radius=[10])

        # Gradient bar (simulate light from top)
        Color(0.3, 0.8, 0.3)
        Rectangle(pos=self.pos, size=(self.width * pct, self.height * 0.9))

        # Highlight/glare strip
        Color(1, 1, 1, 0.15)
        Rectangle(pos=(self.x, self.y + self.height * 0.6), size=(self.width * pct, self.height * 0.3))

        self.label.text = f"{self.value:.1f} {self.units}"

    def _draw_digital(self):
        self.label.text = f"{self.value:.1f} {self.units}"

    def _draw_needle_3d(self):
        center_x = self.center_x
        center_y = self.center_y
        radius = min(self.width, self.height) / 2 - 10

        # Dial face
        Color(0.2, 0.2, 0.2)
        Ellipse(pos=(center_x - radius, center_y - radius), size=(2*radius, 2*radius))

        # Radial shine
        Color(1, 1, 1, 0.1)
        Ellipse(pos=(center_x - radius, center_y - radius), size=(2*radius, 2*radius), angle_start=45, angle_end=135)

        # Needle
        angle_deg = 180 * ((self.value - self.min_val) / (self.max_val - self.min_val))
        angle_deg = max(0, min(180, angle_deg))
        angle_rad = radians(angle_deg)
        x = center_x + radius * cos(angle_rad)
        y = center_y + radius * sin(angle_rad)
        Color(1, 0, 0)
        Line(points=[center_x, center_y, x, y], width=2)

        # Needle shadow
        Color(0, 0, 0, 0.4)
        Line(points=[center_x + 2, center_y - 2, x + 2, y - 2], width=1)

        # Center pin
        Color(1, 1, 1)
        Ellipse(pos=(center_x - 5, center_y - 5), size=(10, 10))

        self.label.text = f"{self.value:.1f} {self.units}"