from kivy.uix.popup import Popup
from dtc_viewer import DTCViewer

class DTCPopup(Popup):
    def __init__(self, dtc_manager, **kwargs):
        super().__init__(title="Diagnostic Trouble Codes", size_hint=(0.8, 0.8), **kwargs)
        self.dtc_manager = dtc_manager
        self.viewer = DTCViewer(self.dtc_manager.get_dtcs())
        self.content = self.viewer

    def update(self):
        self.dtc_manager.update_from_can()
        self.viewer.refresh()