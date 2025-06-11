from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.garden.graph import Graph, LinePlot
from collections import deque
from kivy.clock import Clock

class SensorGraphPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.available_signals = {
            'RPM': [1, 0, 0, 1],
            'Coolant Temp': [0, 0, 1, 1],
            'AFR': [0, 1, 0, 1],
            'Speed': [1, 1, 0, 1],
            'Oil Pressure': [1, 0, 1, 1],
            'Voltage': [0, 1, 1, 1],
        }

        self.data = {k: deque(maxlen=100) for k in self.available_signals}
        self.plots = {}
        self.selected_signals = set()

        self.graph = Graph(xlabel='Time', ylabel='Value', x_ticks_minor=5,
                           x_ticks_major=25, y_ticks_major=10,
                           y_grid_label=True, x_grid_label=True, padding=5,
                           x_grid=True, y_grid=True, xmin=0, xmax=100, ymin=0, ymax=100)
        self.add_widget(self.graph)

        selector = GridLayout(cols=2, size_hint_y=0.3, height=200)
        for signal, color in self.available_signals.items():
            cb = CheckBox()
            cb.bind(active=self.make_toggle_callback(signal, color))
            selector.add_widget(cb)
            selector.add_widget(Label(text=signal, halign='left'))
        self.add_widget(selector)

        Clock.schedule_interval(self.refresh, 0.5)

    def make_toggle_callback(self, signal, color):
        def toggle(checkbox, value):
            if value:
                self.selected_signals.add(signal)
                plot = LinePlot(line_width=1.2, color=color)
                self.graph.add_plot(plot)
                self.plots[signal] = plot
            else:
                self.selected_signals.discard(signal)
                if signal in self.plots:
                    self.graph.remove_plot(self.plots[signal])
                    del self.plots[signal]
        return toggle

    def update_sensor(self, signal, value):
        if signal in self.data:
            self.data[signal].append(value)

    def refresh(self, dt):
        ymin, ymax = None, None
        for signal in self.selected_signals:
            values = list(self.data[signal])
            if not values:
                continue
            self.plots[signal].points = [(i, v) for i, v in enumerate(values)]
            ymin = min(values) if ymin is None else min(ymin, min(values))
            ymax = max(values) if ymax is None else max(ymax, max(values))
        if ymin is not None and ymax is not None:
            self.graph.ymin = ymin - 5
            self.graph.ymax = ymax + 5