import usb_hid
from adafruit_hid.keyboard import Keyboard

# type: ignore
class RasperDuckyKeyboard:
    def __init__(self, platform: str, language: str):
        if platform == "mac":
            if language == "fr":
                from keyboard_layout_mac_fr import KeyboardLayout
                from keycode_mac_fr import Keycode
            else:
                raise ValueError(f"Language {language} not supported for platform {platform}")
        elif platform == "win":
            if language == "br":
                from keyboard_layout_win_br import KeyboardLayout
                from keycode_win_br import Keycode
            elif language == "cz":
                from keyboard_layout_win_cz import KeyboardLayout
                from keycode_win_cz import Keycode
            elif language == "cz1":
                from keyboard_layout_win_cz1 import KeyboardLayout
                from keycode_win_cz1 import Keycode
            elif language == "da":
                from keyboard_layout_win_da import KeyboardLayout
                from keycode_win_da import Keycode
            elif language == "de":
                from keyboard_layout_win_de import KeyboardLayout
                from keycode_win_de import Keycode
            elif language == "es":
                from keyboard_layout_win_es import KeyboardLayout
                from keycode_win_es import Keycode
            elif language == "fr":
                from keyboard_layout_win_fr import KeyboardLayout
                from keycode_win_fr import Keycode
            elif language == "hu":
                from keyboard_layout_win_hu import KeyboardLayout
                from keycode_win_hu import Keycode
            elif language == "it":
                from keyboard_layout_win_it import KeyboardLayout
                from keycode_win_it import Keycode
            elif language == "po":
                from keyboard_layout_win_po import KeyboardLayout
                from keycode_win_po import Keycode
            elif language == "sw":
                from keyboard_layout_win_sw import KeyboardLayout
                from keycode_win_sw import Keycode
            elif language == "tr":
                from keyboard_layout_win_tr import KeyboardLayout
                from keycode_win_tr import Keycode
            elif language == "uk":
                from keyboard_layout_win_uk import KeyboardLayout
                from keycode_win_uk import Keycode
            else:
                raise ValueError(f"Language {language} not supported for platform {platform}")
        else:
            raise ValueError(f"Platform {platform} not supported")
        
        self.kbd = Keyboard(usb_hid.devices)
        self.layout = KeyboardLayout(self.kbd)

        self.KEYCODES = {
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


    def type_string(self, string):
        self.layout.write(string)

    def press_key(self, key: str):
        self.kbd.press(self.KEYCODES[key])

    def release_all(self):
        self.kbd.release_all()
