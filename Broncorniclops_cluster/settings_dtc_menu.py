from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from dtc_popup import DTCPopup

class SettingsMenu(BoxLayout):
    def __init__(self, dtc_manager, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.dtc_manager = dtc_manager

        self.view_dtcs_btn = Button(text="View DTCs")
        self.view_dtcs_btn.bind(on_press=self.view_dtcs)
        self.add_widget(self.view_dtcs_btn)

        self.clear_dtcs_btn = Button(text="Clear All DTCs")
        self.clear_dtcs_btn.bind(on_press=self.clear_dtcs)
        self.add_widget(self.clear_dtcs_btn)

    def view_dtcs(self, instance):
        popup = DTCPopup(self.dtc_manager)
        popup.open()

    def clear_dtcs(self, instance):
        self.dtc_manager.clear_dtcs()