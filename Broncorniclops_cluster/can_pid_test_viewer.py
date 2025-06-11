from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class CANPIDTestViewer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.pid_map = {}  # PID to label mapping
        self.values = {}   # PID to current value
        self.labels = {}   # PID to Label widget

        self.display_grid = GridLayout(cols=2, size_hint_y=None)
        self.display_grid.bind(minimum_height=self.display_grid.setter('height'))

        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.scroll.add_widget(self.display_grid)
        self.add_widget(self.scroll)

        self.label_input = TextInput(hint_text="PID:Label (e.g., 0C:RPM)", multiline=False, size_hint_y=0.1)
        self.label_input.bind(on_text_validate=self.apply_label)
        self.add_widget(self.label_input)

        self.clear_btn = Button(text="Clear Labels", size_hint_y=0.1)
        self.clear_btn.bind(on_press=self.clear_labels)
        self.add_widget(self.clear_btn)

    def apply_label(self, instance):
        try:
            text = self.label_input.text.strip()
            pid, label = text.split(":")
            self.pid_map[pid.strip().upper()] = label.strip()
            self.label_input.text = ""
        except:
            pass

    def clear_labels(self, instance):
        self.pid_map.clear()

    def update_pid(self, pid, value):
        pid = pid.upper()
        label = self.pid_map.get(pid, pid)
        self.values[pid] = value

        if pid not in self.labels:
            pid_label = Label(text=label)
            value_label = Label(text=str(value))
            self.labels[pid] = value_label
            self.display_grid.add_widget(pid_label)
            self.display_grid.add_widget(value_label)
        else:
            self.labels[pid].text = str(value)