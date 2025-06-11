from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from settings_popup import SettingsPopup
from layout_mode_toggle import LayoutModeToggle
from layout_profile_popup import LayoutProfilePopup

class Toolbar(BoxLayout):
    def __init__(self, dtc_manager, layout_editor=None, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=40, **kwargs)
        self.dtc_manager = dtc_manager
        self.layout_editor = layout_editor

        self.settings_btn = Button(text="⚙ Settings")
        self.settings_btn.bind(on_press=self.open_settings)
        self.add_widget(self.settings_btn)

        if self.layout_editor:
            self.add_widget(LayoutModeToggle(self.layout_editor))

            self.profile_btn = Button(text="📁 Layout Profiles")
            self.profile_btn.bind(on_press=self.open_layout_profiles)
            self.add_widget(self.profile_btn)

    def open_settings(self, instance):
        popup = SettingsPopup(dtc_manager=self.dtc_manager, layout_editor=self.layout_editor)
        popup.open()

    def open_layout_profiles(self, instance):
        popup = LayoutProfilePopup(layout_editor=self.layout_editor)
        popup.open()