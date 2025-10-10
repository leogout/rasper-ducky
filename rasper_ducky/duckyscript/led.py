import board
import digitalio


class LED:
    def __init__(self):
        self.led = digitalio.DigitalInOut(board.LED)
        self.led.direction = digitalio.Direction.OUTPUT

    def on(self):
        """Turn the LED on"""
        self.led.value = True

    def off(self):
        """Turn the LED off"""
        self.led.value = False