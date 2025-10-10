import time
import board
import digitalio


class Button:
    def __init__(self, pin=None):
        if pin is None:
            pin = board.GP15
        self.button = digitalio.DigitalInOut(pin)
        self.button.switch_to_input(pull=digitalio.Pull.UP)

    def wait_for_press(self):
        """Wait for button press (transition from HIGH to LOW)"""
        # Wait for button to be released if currently pressed
        while not self.button.value:
            time.sleep(0.01)

        # Wait for button press
        while self.button.value:
            time.sleep(0.01)

        # Debounce
        time.sleep(0.05)