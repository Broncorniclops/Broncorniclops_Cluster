from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from layout_profile_manager import LayoutProfileManager

class LayoutProfilePopup(Popup):
    def __init__(self, layout_editor, **kwargs):
        super().__init__(title="Layout Profiles", size_hint=(0.8, 0.6), **kwargs)
        self.manager = LayoutProfileManager()
        self.layout_editor = layout_editor
        self.box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.spinner = Spinner(text="Select Profile", values=self.manager.list_profiles())
        self.box.add_widget(self.spinner)

        self.name_input = TextInput(hint_text="Enter new profile name", multiline=False)
        self.box.add_widget(self.name_input)

        self.save_btn = Button(text="Save Current Layout")
        self.save_btn.bind(on_press=self.save_profile)
        self.box.add_widget(self.save_btn)

        self.load_btn = Button(text="Load Selected Layout")
        self.load_btn.bind(on_press=self.load_profile)
        self.box.add_widget(self.load_btn)

        self.delete_btn = Button(text="Delete Selected Layout")
        self.delete_btn.bind(on_press=self.delete_profile)
        self.box.add_widget(self.delete_btn)

        self.content = self.box

    def save_profile(self, instance):
        name = self.name_input.text.strip()
        if name:
            layout = self.layout_editor.get_layout()
            self.manager.save_profile(name, layout)
            self.spinner.values = self.manager.list_profiles()

    def load_profile(self, instance):
        name = self.spinner.text.strip()
        if name:
            layout = self.manager.load_profile(name)
            self.layout_editor.clear_widgets()
            for item in layout:
                from layout_editor import DraggableGauge
                g = DraggableGauge(text=item.get("type", "Gauge"))
                g.pos = item["pos"]
                g.size = item["size"]
                self.layout_editor.add_widget(g)

    def delete_profile(self, instance):
        name = self.spinner.text.strip()
        if name:
            self.manager.delete_profile(name)
            self.spinner.values = self.manager.list_profiles()