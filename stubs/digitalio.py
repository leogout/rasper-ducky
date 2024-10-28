from enum import Enum


class Pull(Enum):
    UP = 1


class DigitalInOut:
    def __init__(self, pin):
        pass

    def switch_to_input(self, pull: Pull):
        pass

    @property
    def value(self):
        return True
