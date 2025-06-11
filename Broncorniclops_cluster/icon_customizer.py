import os
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.behaviors import DragBehavior
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

ICON_DIR = "/home/pi/digital_cluster/icons"
os.makedirs(ICON_DIR, exist_ok=True)

class DraggableIcon(DragBehavior, Image):
    def __init__(self, icon_path, **kwargs):
        super().__init__(**kwargs)
        self.source = icon_path
        self.size_hint = (None, None)
        self.size = (64, 64)
        self.drag_timeout = 10000000
        self.drag_distance = 1
        self.drag_rectangle = self.x, self.y, 64, 64

class IconCustomizer(Popup):
    def __init__(self, apply_callback, **kwargs):
        super().__init__(title="Icon Customizer", size_hint=(0.95, 0.95), **kwargs)
        self.apply_callback = apply_callback

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.grid = GridLayout(cols=4, spacing=10, size_hint_y=0.8)
        for fname in sorted(os.listdir(ICON_DIR)):
            if fname.endswith(".png"):
                icon = DraggableIcon(os.path.join(ICON_DIR, fname))
                icon.bind(on_touch_up=self.on_icon_drop)
                self.grid.add_widget(icon)

        layout.add_widget(self.grid)
        layout.add_widget(Label(text="Drag an icon onto a gauge"))

        close_btn = Button(text="Close", size_hint_y=0.1)
        close_btn.bind(on_press=self.dismiss)
        layout.add_widget(close_btn)

        self.content = layout

    def on_icon_drop(self, icon, touch):
        if icon.collide_point(*touch.pos) and touch.grab_current is icon:
            selected_path = icon.source
            self.apply_callback(selected_path)
            self.dismiss()