from gauge_profile_switcher import GaugeProfileSwitcher
from icon_customizer import IconCustomizer
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.uix.label import Label

class DraggableGauge(Label):
    editing = BooleanProperty(False)

    def on_touch_down(self, touch):
        if not self.editing or not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        self._offset_x = touch.x - self.x
        self._offset_y = touch.y - self.y
        return True

    def on_touch_move(self, touch):
        if not self.editing or not hasattr(self, "_offset_x"):
            return super().on_touch_move(touch)
        self.x = touch.x - self._offset_x
        self.y = touch.y - self._offset_y
        return True

class LayoutEditor(FloatLayout):
    edit_mode = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down)

    def add_gauge(self, gauge):
        self.add_widget(gauge)

    def set_edit_mode(self, enabled):
        self.edit_mode = enabled
        for child in self.children:
            if hasattr(child, 'editing'):
                child.editing = enabled

    def get_layout(self):
        return [{
            'type': getattr(child, 'gauge_type', 'unknown'),
            'pos': child.pos,
            'size': child.size
        } for child in self.children if isinstance(child, Widget)]

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 27:  # ESC to exit layout mode
            self.set_edit_mode(False)

    def open_icon_customizer(self, instance=None):
        def apply_icon(path):
            print("Icon selected for layout editor:", path)
        popup = IconCustomizer(apply_callback=apply_icon)
        popup.open()

    def open_profile_switcher(self, instance=None):
        GaugeProfileSwitcher(self.app.layout_manager).open()