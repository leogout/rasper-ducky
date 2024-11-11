import usb_hid
from adafruit_hid.keyboard import Keyboard


# type: ignore
class RasperDuckyKeyboard:
    def __init__(self, platform: str, language: str):
        self.platform = platform
        self.language = language

        try:
            layout = __import__(f"keyboard_layout_{platform}_{language}")
            keycode = __import__(f"keycode_{platform}_{language}")
        except ImportError:
            raise ValueError(
                f"Language {language} not supported for platform {platform}"
            )

        self.kbd = Keyboard(usb_hid.devices)
        self.layout = layout.KeyboardLayout(self.kbd)

        self.KEYCODES = {
            "WINDOWS": keycode.Keycode.WINDOWS,
            "GUI": keycode.Keycode.GUI,
            "APP": keycode.Keycode.APPLICATION,
            "MENU": keycode.Keycode.APPLICATION,
            "SHIFT": keycode.Keycode.SHIFT,
            "ALT": keycode.Keycode.ALT,
            "CONTROL": keycode.Keycode.CONTROL,
            "CTRL": keycode.Keycode.CONTROL,
            "DOWNARROW": keycode.Keycode.DOWN_ARROW,
            "DOWN": keycode.Keycode.DOWN_ARROW,
            "LEFTARROW": keycode.Keycode.LEFT_ARROW,
            "LEFT": keycode.Keycode.LEFT_ARROW,
            "RIGHTARROW": keycode.Keycode.RIGHT_ARROW,
            "RIGHT": keycode.Keycode.RIGHT_ARROW,
            "UPARROW": keycode.Keycode.UP_ARROW,
            "UP": keycode.Keycode.UP_ARROW,
            "BREAK": keycode.Keycode.PAUSE,
            "PAUSE": keycode.Keycode.PAUSE,
            "CAPSLOCK": keycode.Keycode.CAPS_LOCK,
            "DELETE": keycode.Keycode.DELETE,
            "END": keycode.Keycode.END,
            "ESC": keycode.Keycode.ESCAPE,
            "ESCAPE": keycode.Keycode.ESCAPE,
            "HOME": keycode.Keycode.HOME,
            "INSERT": keycode.Keycode.INSERT,
            "NUMLOCK": keycode.Keycode.KEYPAD_NUMLOCK,
            "PAGEUP": keycode.Keycode.PAGE_UP,
            "PAGEDOWN": keycode.Keycode.PAGE_DOWN,
            "PRINTSCREEN": keycode.Keycode.PRINT_SCREEN,
            "ENTER": keycode.Keycode.ENTER,
            "SCROLLLOCK": keycode.Keycode.SCROLL_LOCK,
            "SPACE": keycode.Keycode.SPACE,
            "TAB": keycode.Keycode.TAB,
            "BACKSPACE": keycode.Keycode.BACKSPACE,
            "A": keycode.Keycode.A,
            "B": keycode.Keycode.B,
            "C": keycode.Keycode.C,
            "D": keycode.Keycode.D,
            "E": keycode.Keycode.E,
            "F": keycode.Keycode.F,
            "G": keycode.Keycode.G,
            "H": keycode.Keycode.H,
            "I": keycode.Keycode.I,
            "J": keycode.Keycode.J,
            "K": keycode.Keycode.K,
            "L": keycode.Keycode.L,
            "M": keycode.Keycode.M,
            "N": keycode.Keycode.N,
            "O": keycode.Keycode.O,
            "P": keycode.Keycode.P,
            "Q": keycode.Keycode.Q,
            "R": keycode.Keycode.R,
            "S": keycode.Keycode.S,
            "T": keycode.Keycode.T,
            "U": keycode.Keycode.U,
            "V": keycode.Keycode.V,
            "W": keycode.Keycode.W,
            "X": keycode.Keycode.X,
            "Y": keycode.Keycode.Y,
            "Z": keycode.Keycode.Z,
            "F1": keycode.Keycode.F1,
            "F2": keycode.Keycode.F2,
            "F3": keycode.Keycode.F3,
            "F4": keycode.Keycode.F4,
            "F5": keycode.Keycode.F5,
            "F6": keycode.Keycode.F6,
            "F7": keycode.Keycode.F7,
            "F8": keycode.Keycode.F8,
            "F9": keycode.Keycode.F9,
            "F10": keycode.Keycode.F10,
            "F11": keycode.Keycode.F11,
            "F12": keycode.Keycode.F12,
        }

    def type_string(self, string):
        self.layout.write(string)

    def press_key(self, key: str):
        self.kbd.press(self.KEYCODES[key])
    
    def release_key(self, key: str):
        self.kbd.release(self.KEYCODES[key])

    def release_all(self):
        self.kbd.release_all()
