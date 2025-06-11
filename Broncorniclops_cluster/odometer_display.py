from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from odometer_manager import OdometerManager

class OdometerDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.manager = OdometerManager()

        self.odo_label = Label(text=f"ODO: {self.manager.odo:.1f} mi", font_size='24sp')
        self.trip_label = Label(text=f"TRIP: {self.manager.trip:.1f} mi", font_size='24sp')

        self.reset_btn = Button(text="Reset Trip")
        self.reset_btn.bind(on_press=self.reset_trip)

        self.edit_btn = Button(text="Edit Odometer")
        self.edit_btn.bind(on_press=self.prompt_odo_edit)

        self.add_widget(self.odo_label)
        self.add_widget(self.trip_label)
        self.add_widget(self.reset_btn)
        self.add_widget(self.edit_btn)

    def update(self):
        self.odo_label.text = f"ODO: {self.manager.odo:.1f} mi"
        self.trip_label.text = f"TRIP: {self.manager.trip:.1f} mi"

    def reset_trip(self, instance):
        self.manager.reset_trip()
        self.update()

    def prompt_odo_edit(self, instance):
        content = BoxLayout(orientation='vertical', spacing=5)
        username = TextInput(hint_text="Username", multiline=False)
        password = TextInput(hint_text="Password", password=True, multiline=False)
        new_val = TextInput(hint_text="New odometer value", multiline=False, input_filter='float')

        submit = Button(text="Apply")
        status = Label(text="")

        def submit_action(_):
            if self.manager.force_set_odo(float(new_val.text), username.text, password.text):
                status.text = "Odometer updated"
                self.update()
            else:
                status.text = "Access denied"

        submit.bind(on_press=submit_action)
        content.add_widget(username)
        content.add_widget(password)
        content.add_widget(new_val)
        content.add_widget(submit)
        content.add_widget(status)

        popup = Popup(title="Edit Odometer", content=content, size_hint=(0.8, 0.6))
        popup.open()