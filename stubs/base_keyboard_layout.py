from adafruit_hid.keyboard import Keyboard


class BaseKeyboardLayout:
    def __init__(self, keyboard: Keyboard):
        self.keyboard = keyboard

    def write(self, string: str):
        """Type the string using the keyboard layout"""
        for char in string:
            # In a real implementation, this would map characters to correct keycodes
            # For stub purposes, we just pass
            pass
