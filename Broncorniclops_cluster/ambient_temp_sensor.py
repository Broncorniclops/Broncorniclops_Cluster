import Adafruit_DHT

class AmbientTempSensor:
    def __init__(self, pin=4):
        self.sensor = Adafruit_DHT.AM2302
        self.pin = pin

    def read_temperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        return temperature if temperature is not None else 50.0