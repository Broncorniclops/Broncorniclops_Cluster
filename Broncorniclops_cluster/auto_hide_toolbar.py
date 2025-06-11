from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.core.window import Window

from toolbar import Toolbar

class AutoHideToolbarContainer(FloatLayout):
    hide_delay = NumericProperty(8)

    def __init__(self, dtc_manager, layout_editor, **kwargs):
        super().__init__(**kwargs)
        self.toolbar = Toolbar(dtc_manager, layout_editor)
        self.toolbar.pos_hint = {'top': 1}
        self.toolbar.size_hint_y = None
        self.toolbar.height = 40
        self.add_widget(self.toolbar)

        self.touch_zone = Widget(size_hint=(1, None), height=10, pos_hint={'top': 1})
        self.touch_zone.bind(on_touch_down=self.on_touch_zone_touch)
        self.add_widget(self.touch_zone)

        Clock.schedule_once(self.hide_toolbar, self.hide_delay)

    def on_touch_zone_touch(self, instance, touch):
        if self.touch_zone.collide_point(*touch.pos):
            self.show_toolbar()
        return False

    def show_toolbar(self):
        self.toolbar.opacity = 1
        self.toolbar.disabled = False
        Clock.unschedule(self.hide_toolbar)
        Clock.schedule_once(self.hide_toolbar, self.hide_delay)

    def hide_toolbar(self, *args):
        self.toolbar.opacity = 0
        self.toolbar.disabled = True