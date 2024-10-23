from unittest.mock import MagicMock


class Keyboard(MagicMock):
    def __init__(self, args):
        pass

    def press(self, key: str):
        pass

    def release(self, key: str):
        pass

    def release_all(self):
        pass
