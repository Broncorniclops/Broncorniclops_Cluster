import board
import busio
import adafruit_tsl2591

class BrightnessControl:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_tsl2591.TSL2591(i2c)

    def read_lux(self):
        return self.sensor.lux

    def compute_brightness(self):
        lux = self.read_lux()
        if lux < 10:
            return 0.1
        elif lux > 1000:
            return 1.0
        else:
            return min(1.0, lux / 1000.0)