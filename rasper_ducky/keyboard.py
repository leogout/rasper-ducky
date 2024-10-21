import usb_hid
from adafruit_hid.keyboard import Keyboard

# comment out these lines for non_US keyboards
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)


def type_string(string):
    layout.write(string)


def press_key(key):
    kbd.press(key)


def release_all():
    kbd.release_all()
