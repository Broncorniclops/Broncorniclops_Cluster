import time
from collections import deque

class MPGFuelEstimator:
    def __init__(self, buffer_size=10):
        self.last_time = None
        self.total_miles = 0.0
        self.total_gallons = 0.0
        self.mpg_buffer = deque(maxlen=buffer_size)  # for smoothing

    def update(self, speed_mph, fuel_rate_gph):
        now = time.time()
        if self.last_time is None or fuel_rate_gph <= 0:
            self.last_time = now
            return

        dt_hours = (now - self.last_time) / 3600.0
        self.last_time = now

        miles = speed_mph * dt_hours
        gallons = fuel_rate_gph * dt_hours

        self.total_miles += miles
        self.total_gallons += gallons

        instant_mpg = (speed_mph / fuel_rate_gph) if fuel_rate_gph > 0 else 0
        self.mpg_buffer.append(instant_mpg)

    def get_smoothed_mpg(self):
        if not self.mpg_buffer:
            return 0.0
        return sum(self.mpg_buffer) / len(self.mpg_buffer)

    def get_trip_mpg(self):
        if self.total_gallons == 0:
            return 0.0
        return self.total_miles / self.total_gallons

    def reset_trip(self):
        self.total_miles = 0.0
        self.total_gallons = 0.0
        self.mpg_buffer.clear()