class GestureManager:
    def __init__(self):
        self._two_finger_swipe_down_callback = None

    def register_two_finger_swipe_down(self, callback):
        self._two_finger_swipe_down_callback = callback

    def handle_touch(self, touches):
        if len(touches) == 2:
            if self._two_finger_swipe_down_callback:
                self._two_finger_swipe_down_callback()