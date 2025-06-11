from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from mpg_estimator import MPGFuelEstimator

class MPGPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.estimator = MPGFuelEstimator()

        self.smoothed_label = Label(text="Current MPG: --", font_size='24sp')
        self.trip_label = Label(text="Trip MPG: --", font_size='24sp')

        self.add_widget(self.smoothed_label)
        self.add_widget(self.trip_label)

        self.reset_btn = Button(text="Reset Trip", size_hint=(1, 0.2))
        self.reset_btn.bind(on_press=self.reset_trip)
        self.add_widget(self.reset_btn)

    def update(self, speed_mph, fuel_rate_gph):
        self.estimator.update(speed_mph, fuel_rate_gph)
        smoothed = self.estimator.get_smoothed_mpg()
        trip = self.estimator.get_trip_mpg()
        self.smoothed_label.text = f"Current MPG: {smoothed:.1f}"
        self.trip_label.text = f"Trip MPG: {trip:.1f}"

    def reset_trip(self, *args):
        self.estimator.reset()