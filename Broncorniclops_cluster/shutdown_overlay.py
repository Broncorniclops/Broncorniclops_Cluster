import os
import socket
import threading
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

SOCKET_PATH = "/tmp/ups_notify.sock"

class ShutdownOverlay(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.opacity = 0
        self.label = Label(text="Shutdown pending...", font_size='28sp', color=(1, 0, 0, 1))
        self.add_widget(self.label)
        with self.canvas.before:
            Color(0, 0, 0, 0.7)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def show(self):
        self.opacity = 1

    def hide(self):
        self.opacity = 0

def start_shutdown_listener(overlay):
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(1)

    def listen_loop():
        while True:
            conn, _ = server.accept()
            msg = conn.recv(1024)
            if msg == b"shutdown_pending":
                overlay.show()
            conn.close()

    thread = threading.Thread(target=listen_loop, daemon=True)
    thread.start()