import usb_hid
from adafruit_hid.keyboard import Keyboard

# comment out these lines for non_US keyboards
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)


KEYCODES = {
    "WINDOWS": Keycode.WINDOWS,
    "GUI": Keycode.GUI,
    "APP": Keycode.APPLICATION,
    "MENU": Keycode.APPLICATION,
    "SHIFT": Keycode.SHIFT,
    "ALT": Keycode.ALT,
    "CONTROL": Keycode.CONTROL,
    "CTRL": Keycode.CONTROL,
    "DOWNARROW": Keycode.DOWN_ARROW,
    "DOWN": Keycode.DOWN_ARROW,
    "LEFTARROW": Keycode.LEFT_ARROW,
    "LEFT": Keycode.LEFT_ARROW,
    "RIGHTARROW": Keycode.RIGHT_ARROW,
    "RIGHT": Keycode.RIGHT_ARROW,
    "UPARROW": Keycode.UP_ARROW,
    "UP": Keycode.UP_ARROW,
    "BREAK": Keycode.PAUSE,
    "PAUSE": Keycode.PAUSE,
    "CAPSLOCK": Keycode.CAPS_LOCK,
    "DELETE": Keycode.DELETE,
    "END": Keycode.END,
    "ESC": Keycode.ESCAPE,
    "ESCAPE": Keycode.ESCAPE,
    "HOME": Keycode.HOME,
    "INSERT": Keycode.INSERT,
    "NUMLOCK": Keycode.KEYPAD_NUMLOCK,
    "PAGEUP": Keycode.PAGE_UP,
    "PAGEDOWN": Keycode.PAGE_DOWN,
    "PRINTSCREEN": Keycode.PRINT_SCREEN,
    "ENTER": Keycode.ENTER,
    "SCROLLLOCK": Keycode.SCROLL_LOCK,
    "SPACE": Keycode.SPACE,
    "TAB": Keycode.TAB,
    "BACKSPACE": Keycode.BACKSPACE,
    "A": Keycode.A,
    "B": Keycode.B,
    "C": Keycode.C,
    "D": Keycode.D,
    "E": Keycode.E,
    "F": Keycode.F,
    "G": Keycode.G,
    "H": Keycode.H,
    "I": Keycode.I,
    "J": Keycode.J,
    "K": Keycode.K,
    "L": Keycode.L,
    "M": Keycode.M,
    "N": Keycode.N,
    "O": Keycode.O,
    "P": Keycode.P,
    "Q": Keycode.Q,
    "R": Keycode.R,
    "S": Keycode.S,
    "T": Keycode.T,
    "U": Keycode.U,
    "V": Keycode.V,
    "W": Keycode.W,
    "X": Keycode.X,
    "Y": Keycode.Y,
    "Z": Keycode.Z,
    "F1": Keycode.F1,
    "F2": Keycode.F2,
    "F3": Keycode.F3,
    "F4": Keycode.F4,
    "F5": Keycode.F5,
    "F6": Keycode.F6,
    "F7": Keycode.F7,
    "F8": Keycode.F8,
    "F9": Keycode.F9,
    "F10": Keycode.F10,
    "F11": Keycode.F11,
    "F12": Keycode.F12,
}


def type_string(string):
    layout.write(string)


def press_key(key: str):
    kbd.press(KEYCODES[key])


def release_all():
    kbd.release_all()
