import os

class FanController:
    def __init__(self, gpio_pwm_cpu, gpio_pwm_ambient, ambient_sensor):
        self.cpu_pin = gpio_pwm_cpu
        self.ambient_sensor = ambient_sensor
        self.ambient_pin = gpio_pwm_ambient
        self.last_cpu_temp = 0
        self.last_ambient_temp = 0

    def get_cpu_temp(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                return int(f.read().strip()) / 1000.0
        except:
            return 50.0  # fallback

    def get_ambient_temp(self):
        return self.ambient_sensor.read_temperature()  # Assumes sensor object passed in

    def compute_pwm(self, temp):
        if temp < 40:
            return 0
        elif temp > 70:
            return 100
        else:
            return int((temp - 40) * 100 / 30)

    def smooth_pwm(self, current, last):
        alpha = 0.3
        return int(alpha * current + (1 - alpha) * last)

    def update_fans(self):
        cpu_temp = self.get_cpu_temp()
        ambient_temp = self.get_ambient_temp()

        pwm_cpu = self.compute_pwm(cpu_temp)
        pwm_ambient = self.compute_pwm(ambient_temp)

        pwm_cpu = self.smooth_pwm(pwm_cpu, self.last_cpu_temp)
        pwm_ambient = self.smooth_pwm(pwm_ambient, self.last_ambient_temp)

        self.last_cpu_temp = pwm_cpu
        self.last_ambient_temp = pwm_ambient

        print(f"Set CPU fan to {pwm_cpu}%")
        print(f"Set Ambient fan to {pwm_ambient}%")