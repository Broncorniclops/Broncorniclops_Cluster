import time
import statistics

class SmoothedSensor:
    def __init__(self, pid_key, can_data, buffer_size=10, min_valid=None, max_valid=None):
        self.pid_key = pid_key
        self.can_data = can_data
        self.buffer = []
        self.buffer_size = buffer_size
        self.min_valid = min_valid
        self.max_valid = max_valid

    def read(self):
        value = self.can_data.get(self.pid_key)
        if value is None or (self.min_valid is not None and value < self.min_valid) or            (self.max_valid is not None and value > self.max_valid):
            return None  # Fault
        self.buffer.append(value)
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)
        return statistics.mean(self.buffer)

    def is_fault(self):
        value = self.can_data.get(self.pid_key)
        return value is None or                (self.min_valid is not None and value < self.min_valid) or                (self.max_valid is not None and value > self.max_valid)

class SensorManager:
    def __init__(self, can_data):
        self.can_data = can_data
        self.sensors = {
            "rpm": SmoothedSensor("RPM", can_data, min_valid=0, max_valid=8000),
            "speed": SmoothedSensor("SPEED_MPH", can_data, min_valid=0, max_valid=140),
            "coolant_temp": SmoothedSensor("COOLANT_TEMP", can_data, min_valid=-40, max_valid=250),
            "oil_pressure": SmoothedSensor("OIL_PRESSURE", can_data, min_valid=0, max_valid=100),
            "voltage": SmoothedSensor("VOLTAGE", can_data, min_valid=0, max_valid=16),
            "trans_temp": SmoothedSensor("TRANS_TEMP", can_data, min_valid=-40, max_valid=250),
            "afr": SmoothedSensor("AFR", can_data, min_valid=0, max_valid=25),
        }

    def read_all(self):
        return {key: sensor.read() for key, sensor in self.sensors.items()}

    def get_faults(self):
        return {key: sensor.is_fault() for key, sensor in self.sensors.items()}