from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

class LayoutModeToggle(BoxLayout):
    def __init__(self, layout_editor, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=40, **kwargs)
        self.layout_editor = layout_editor
        self.toggle = ToggleButton(text='Layout Edit: OFF', state='normal')
        self.toggle.bind(on_press=self.toggle_mode)
        self.add_widget(self.toggle)

    def toggle_mode(self, instance):
        is_editing = instance.state == 'down'
        self.layout_editor.set_edit_mode(is_editing)
        self.toggle.text = 'Layout Edit: ON' if is_editing else 'Layout Edit: OFF'