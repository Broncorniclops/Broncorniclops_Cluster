from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from style_manager import StyleManager

class StyleSettingsPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.manager = StyleManager()

        self.add_widget(Label(text="Theme"))
        self.theme_spinner = Spinner(text=self.manager.current_theme, values=["light", "dark"])
        self.theme_spinner.bind(text=self.update_theme)
        self.add_widget(self.theme_spinner)

        self.add_widget(Label(text="Font"))
        self.font_input = TextInput(text=self.manager.get_font(), multiline=False)
        self.font_input.bind(on_text_validate=self.update_font)
        self.add_widget(self.font_input)

        self.add_widget(Label(text="Background Color"))
        self.bg_input = TextInput(text=self.manager.get_color("bg"), multiline=False)
        self.bg_input.bind(on_text_validate=self.update_colors)
        self.add_widget(self.bg_input)

        self.add_widget(Label(text="Foreground Color"))
        self.fg_input = TextInput(text=self.manager.get_color("fg"), multiline=False)
        self.fg_input.bind(on_text_validate=self.update_colors)
        self.add_widget(self.fg_input)

        self.add_widget(Label(text="Accent Color"))
        self.accent_input = TextInput(text=self.manager.get_color("accent"), multiline=False)
        self.accent_input.bind(on_text_validate=self.update_colors)
        self.add_widget(self.accent_input)

        self.save_button = Button(text="Apply + Save")
        self.save_button.bind(on_press=self.save_all)
        self.add_widget(self.save_button)

    def update_theme(self, spinner, text):
        self.manager.set_theme(text)

    def update_font(self, instance):
        self.manager.set_font(instance.text)

    def update_colors(self, instance=None):
        self.manager.set_color("bg", self.bg_input.text)
        self.manager.set_color("fg", self.fg_input.text)
        self.manager.set_color("accent", self.accent_input.text)

    def save_all(self, instance):
        self.update_colors()
        self.update_font(self.font_input)
        self.update_theme(self.theme_spinner, self.theme_spinner.text)