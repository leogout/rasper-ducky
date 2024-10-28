from unittest.mock import MagicMock

from adafruit_hid.keycode import Keycode


class Keyboard(MagicMock):
    def __init__(self, args):
        pass

    def press(self, key: Keycode):
        pass

    def release(self, key: Keycode):
        pass

    def release_all(self):
        pass
