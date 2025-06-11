from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class DiagnosticsOverlay(BoxLayout):
    def __init__(self, fan_controller, ambient_sensor, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.fan_controller = fan_controller
        self.ambient_sensor = ambient_sensor

        self.cpu_temp_label = Label(text='CPU Temp: --°C')
        self.ambient_temp_label = Label(text='Ambient Temp: --°C')
        self.cpu_fan_label = Label(text='CPU Fan: --%')
        self.ambient_fan_label = Label(text='Ambient Fan: --%')

        self.add_widget(self.cpu_temp_label)
        self.add_widget(self.ambient_temp_label)
        self.add_widget(self.cpu_fan_label)
        self.add_widget(self.ambient_fan_label)

    def update(self):
        cpu_temp = self.fan_controller.get_cpu_temp()
        ambient_temp = self.ambient_sensor.read_temperature()
        cpu_pwm = self.fan_controller.last_cpu_temp
        ambient_pwm = self.fan_controller.last_ambient_temp

        self.cpu_temp_label.text = f'CPU Temp: {cpu_temp:.1f}°C'
        self.ambient_temp_label.text = f'Ambient Temp: {ambient_temp:.1f}°C'
        self.cpu_fan_label.text = f'CPU Fan: {cpu_pwm}%'
        self.ambient_fan_label.text = f'Ambient Fan: {ambient_pwm}%'