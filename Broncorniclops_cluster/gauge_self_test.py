from kivy.clock import Clock

class GaugeSelfTest:
    def __init__(self, gauges):
        self.gauges = gauges  # Dictionary of gauge widgets
        self.state = 0
        self.delay = 0.05
        self.test_values = {}

    def start(self):
        self.state = 0
        self.test_values = {k: v.value for k, v in self.gauges.items() if hasattr(v, 'value')}
        Clock.schedule_interval(self.animate_step, self.delay)

    def animate_step(self, dt):
        done = True
        for gauge in self.gauges.values():
            if hasattr(gauge, 'value'):
                max_val = getattr(gauge, 'max', 100)
                step = max_val / 20
                if self.state == 0 and gauge.value < max_val:
                    gauge.value += step
                    done = False
                elif self.state == 1 and gauge.value > 0:
                    gauge.value -= step
                    done = False
        if done:
            if self.state == 0:
                self.state = 1
                return False  # pause, then restart
            else:
                for k, v in self.test_values.items():
                    if hasattr(self.gauges[k], 'value'):
                        self.gauges[k].value = v
                return False  # test complete
        return True
    def start_loop_until_boot(self, parent):
        self.parent = parent
        self._original = {k: v.value for k, v in self.gauges.items() if hasattr(v, 'value')}
        self._loop()

    def _loop(self):
        self.state = 0
        Clock.schedule_interval(self.animate_step, self.delay)

    def animate_step(self, dt):
        done = True
        for gauge in self.gauges.values():
            if hasattr(gauge, 'value'):
                max_val = getattr(gauge, 'max', 100)
                step = max_val / 20
                if self.state == 0 and gauge.value < max_val:
                    gauge.value += step
                    done = False
                elif self.state == 1 and gauge.value > 0:
                    gauge.value -= step
                    done = False
        if done:
            if self.state == 0:
                self.state = 1
                return True
            else:
                for k, v in self._original.items():
                    if hasattr(self.gauges[k], 'value'):
                        self.gauges[k].value = v
                if self.parent.boot_complete:
                    return False
                else:
                    Clock.schedule_once(lambda dt: self._loop(), 0.5)
                    return False
        return True
