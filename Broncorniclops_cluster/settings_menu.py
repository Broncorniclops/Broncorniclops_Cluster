from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from settings_dtc_menu import SettingsMenu as DTCSettings
from style_settings_panel import StyleSettingsPanel

class SettingsMenu(BoxLayout):
    def __init__(self, dtc_manager, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.dtc_settings = DTCSettings(dtc_manager)
        self.style_settings = StyleSettingsPanel()

        self.add_widget(Button(text="--- DTC Settings ---", size_hint_y=None, height=30))
        self.add_widget(self.dtc_settings)

        self.add_widget(Button(text="--- UI Style Settings ---", size_hint_y=None, height=30))
        self.add_widget(self.style_settings)