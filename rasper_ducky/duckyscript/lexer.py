class Tok:
    VAR = "VAR"
    DELAY = "DELAY"
    IDENTIFIER = "IDENTIFIER"
    ASSIGN = "ASSIGN"
    SKIP = "SKIP"
    MISMATCH = "MISMATCH"
    PRINTSTRING = "PRINTSTRING"
    PRINTSTRINGLN = "PRINTSTRINGLN"
    EOF = "EOF"
    EOL = "EOL"
    KEYPRESS = "KEYPRESS"
    REM = "REM"
    REM_BLOCK = "REM_BLOCK"
    END_REM_BLOCK = "END_REM_BLOCK"

    WAIT_FOR_BUTTON_PRESS = "WAIT_FOR_BUTTON_PRESS"
    
    HOLD = "HOLD"
    RELEASE = "RELEASE"

    RANDOM_CHAR = "RANDOM_CHAR"
    RANDOM_CHAR_FROM = "RANDOM_CHAR_FROM"

    ATTACKMODE = "ATTACKMODE"
    HID = "HID"
    STORAGE = "STORAGE"
    OFF = "OFF"

    IF = "IF"
    THEN = "THEN"
    END_IF = "END_IF"
    ELSE = "ELSE"
    ELSE_IF = "ELSE_IF"

    WHILE = "WHILE"
    END_WHILE = "END_WHILE"

    LPAREN = "LPAREN"
    RPAREN = "RPAREN"

    FUNCTION = "FUNCTION"
    END_FUNCTION = "END_FUNCTION"
    RETURN = "RETURN"

    # OPERATORS
    OP_SHIFT_LEFT = "OP_SHIFT_LEFT"
    OP_SHIFT_RIGHT = "OP_SHIFT_RIGHT"
    OP_GREATER_EQUAL = "OP_GREATER_EQUAL"
    OP_LESS_EQUAL = "OP_LESS_EQUAL"
    OP_EQUAL = "OP_EQUAL"
    OP_NOT_EQUAL = "OP_NOT_EQUAL"
    OP_GREATER = "OP_GREATER"
    OP_LESS = "OP_LESS"
    OP_OR = "OP_OR"
    OP_BITWISE_AND = "OP_BITWISE_AND"
    OP_BITWISE_OR = "OP_BITWISE_OR"
    OP_PLUS = "OP_PLUS"
    OP_MINUS = "OP_MINUS"
    OP_MULTIPLY = "OP_MULTIPLY"
    OP_DIVIDE = "OP_DIVIDE"
    OP_MODULO = "OP_MODULO"
    OP_POWER = "OP_POWER"
    OP_NOT = "OP_NOT"
    OP_AND = "OP_AND"

    # LITERALS
    STRING = "STRING"
    NUMBER = "NUMBER"
    TRUE = "TRUE"
    FALSE = "FALSE"

    # CUSTOM RASPER DUCKY COMMANDS (non rubber ducky standards)
    RD_KBD = "RD_KBD"
    RD_KBD_PLATFORM = "RD_KBD_PLATFORM"
    RD_KBD_LANGUAGE = "RD_KBD_LANGUAGE"


class Token:
    def __init__(self, type: str, value: str = "", line: int = 0, column: int = 0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __repr__(self) -> str:
        return f"TOKEN({self.type}, {self.value}, {self.line}, {self.column})"


class Lexer:
    OPERATORS = {
        "=": Tok.ASSIGN,
        "==": Tok.OP_EQUAL,
        "!=": Tok.OP_NOT_EQUAL,
        ">": Tok.OP_GREATER,
        "<": Tok.OP_LESS,
        ">=": Tok.OP_GREATER_EQUAL,
        "<=": Tok.OP_LESS_EQUAL,
        "&&": Tok.OP_AND,
        "||": Tok.OP_OR,
        "!": Tok.OP_NOT,
        "+": Tok.OP_PLUS,
        "-": Tok.OP_MINUS,
        "*": Tok.OP_MULTIPLY,
        "/": Tok.OP_DIVIDE,
        "%": Tok.OP_MODULO,
        "^": Tok.OP_POWER,
        "&": Tok.OP_BITWISE_AND,
        "|": Tok.OP_BITWISE_OR,
        "<<": Tok.OP_SHIFT_LEFT,
        ">>": Tok.OP_SHIFT_RIGHT,
        "(": Tok.LPAREN,
        ")": Tok.RPAREN,
    }

    OPERATORS_SET = set("=><!&|^+-*/%^&|()")

    KEYWORDS = {
        "RD_KBD": Tok.RD_KBD,
        "VAR": Tok.VAR,
        "IF": Tok.IF,
        "THEN": Tok.THEN,
        "END_IF": Tok.END_IF,
        "ELSE": Tok.ELSE,
        "ELSE IF": Tok.ELSE_IF,
        "WHILE": Tok.WHILE,
        "END_WHILE": Tok.END_WHILE,
        "DELAY": Tok.DELAY,
        "STRING": Tok.PRINTSTRING,
        "STRINGLN": Tok.PRINTSTRINGLN,
        "HOLD": Tok.HOLD,
        "RELEASE": Tok.RELEASE,
        "WAIT_FOR_BUTTON_PRESS": Tok.WAIT_FOR_BUTTON_PRESS,
        "RANDOM_LOWERCASE_LETTER": Tok.RANDOM_CHAR,
        "RANDOM_UPPERCASE_LETTER": Tok.RANDOM_CHAR,
        "RANDOM_LETTER": Tok.RANDOM_CHAR,
        "RANDOM_NUMBER": Tok.RANDOM_CHAR,
        "RANDOM_SPECIAL": Tok.RANDOM_CHAR,
        "RANDOM_CHAR": Tok.RANDOM_CHAR,
        "RANDOM_CHAR_FROM": Tok.RANDOM_CHAR_FROM,
        "ATTACKMODE": Tok.ATTACKMODE,
        "HID": Tok.HID,
        "STORAGE": Tok.STORAGE,
        "OFF": Tok.OFF,
        "FUNCTION": Tok.FUNCTION,
        "END_FUNCTION": Tok.END_FUNCTION,
        "RETURN": Tok.RETURN,
        "TRUE": Tok.TRUE,
        "FALSE": Tok.FALSE,
        "REM": Tok.REM,
        "REM_BLOCK": Tok.REM_BLOCK,
        "END_REM": Tok.END_REM_BLOCK,
        "WINDOWS": Tok.KEYPRESS,
        "GUI": Tok.KEYPRESS,
        "APP": Tok.KEYPRESS,
        "MENU": Tok.KEYPRESS,
        "SHIFT": Tok.KEYPRESS,
        "ALT": Tok.KEYPRESS,
        "CONTROL": Tok.KEYPRESS,
        "CTRL": Tok.KEYPRESS,
        "DOWNARROW": Tok.KEYPRESS,
        "DOWN": Tok.KEYPRESS,
        "LEFTARROW": Tok.KEYPRESS,
        "LEFT": Tok.KEYPRESS,
        "RIGHTARROW": Tok.KEYPRESS,
        "RIGHT": Tok.KEYPRESS,
        "UPARROW": Tok.KEYPRESS,
        "UP": Tok.KEYPRESS,
        "BREAK": Tok.KEYPRESS,
        "PAUSE": Tok.KEYPRESS,
        "CAPSLOCK": Tok.KEYPRESS,
        "DELETE": Tok.KEYPRESS,
        "END": Tok.KEYPRESS,
        "ESCAPE": Tok.KEYPRESS,
        "ESC": Tok.KEYPRESS,
        "HOME": Tok.KEYPRESS,
        "INSERT": Tok.KEYPRESS,
        "NUMLOCK": Tok.KEYPRESS,
        "PAGEUP": Tok.KEYPRESS,
        "PAGEDOWN": Tok.KEYPRESS,
        "PRINTSCREEN": Tok.KEYPRESS,
        "ENTER": Tok.KEYPRESS,
        "SCROLLLOCK": Tok.KEYPRESS,
        "SPACE": Tok.KEYPRESS,
        "TAB": Tok.KEYPRESS,
        "BACKSPACE": Tok.KEYPRESS,
        "F12": Tok.KEYPRESS,
        "F11": Tok.KEYPRESS,
        "F10": Tok.KEYPRESS,
        "F9": Tok.KEYPRESS,
        "F8": Tok.KEYPRESS,
        "F7": Tok.KEYPRESS,
        "F6": Tok.KEYPRESS,
        "F5": Tok.KEYPRESS,
        "F4": Tok.KEYPRESS,
        "F3": Tok.KEYPRESS,
        "F2": Tok.KEYPRESS,
        "F1": Tok.KEYPRESS,
        "A": Tok.KEYPRESS,
        "B": Tok.KEYPRESS,
        "C": Tok.KEYPRESS,
        "D": Tok.KEYPRESS,
        "E": Tok.KEYPRESS,
        "F": Tok.KEYPRESS,
        "G": Tok.KEYPRESS,
        "H": Tok.KEYPRESS,
        "I": Tok.KEYPRESS,
        "J": Tok.KEYPRESS,
        "K": Tok.KEYPRESS,
        "L": Tok.KEYPRESS,
        "M": Tok.KEYPRESS,
        "N": Tok.KEYPRESS,
        "O": Tok.KEYPRESS,
        "P": Tok.KEYPRESS,
        "Q": Tok.KEYPRESS,
        "R": Tok.KEYPRESS,
        "S": Tok.KEYPRESS,
        "T": Tok.KEYPRESS,
        "U": Tok.KEYPRESS,
        "V": Tok.KEYPRESS,
        "W": Tok.KEYPRESS,
        "X": Tok.KEYPRESS,
        "Y": Tok.KEYPRESS,
        "Z": Tok.KEYPRESS,
    }

    def __init__(self, code: str):
        self.code = code
        self.current = 0
        self.start = 0
        self.line = 1
        self.line_start = 0
        self.end = len(code)

    def is_at_end(self):
        return self.current >= self.end

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.code[self.current - 1]

    def previous(self):
        return self.code[self.current - 1] if self.current > 0 else None

    def peek(self):
        return self.code[self.current] if not self.is_at_end() else None

    def peek_next(self):
        return self.code[self.current + 1] if self.current + 1 < self.end else None

    def match(self, expected: str):
        if self.is_at_end() or not self.code.startswith(expected, self.current):
            return False
        self.current += len(expected)
        return True

    def tokenize(self):
        previous_token = None
        while not self.is_at_end():
            self.start = self.current
            previous_token = self.scan_token(previous_token)
            if previous_token:
                yield previous_token
        yield Token(Tok.EOF)

    def is_digit(self, char: str | None):
        return char.isdigit() if char else False

    def is_alpha(self, char: str | None):
        return char.isalpha() or char in "$_" if char else False

    def is_alphanumeric(self, char: str | None):
        return self.is_digit(char) or self.is_alpha(char)

    def is_operator(self, char: str | None):
        return char in self.OPERATORS_SET if char else False

    def is_comment(self, char: str | None):
        if char is None:
            return False
        return char == "R" and self.match("EM")

    def is_comment_block(self, char: str | None):
        if char is None:
            return False
        return char == "R" and self.match("EM_BLOCK")

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()

        return self.token(Tok.NUMBER, self.code[self.start : self.current])

    def string(self):
        # Skip the first space between STRING or STRINGLN and the string
        self.start += 1
        self.advance_while(lambda c: c != "\n")
        return self.token(Tok.STRING, self.code[self.start : self.current].strip())

    def kbd_platform(self):
        self.start += 1
        self.advance_while(lambda c: c != " ")
        return self.token(
            Tok.RD_KBD_PLATFORM, self.code[self.start : self.current].strip()
        )

    def kbd_language(self):
        self.start += 1
        self.advance_while(lambda c: c != "\n")
        return self.token(
            Tok.RD_KBD_LANGUAGE, self.code[self.start : self.current].strip()
        )

    def identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()

        identifier = self.code[self.start : self.current]
        keyword = self.KEYWORDS.get(identifier)

        if keyword == Tok.ELSE and self.peek() == " ":
            self.advance_while(lambda c: c == " ")
            if self.match("IF"):
                return self.token(Tok.ELSE_IF, "ELSE IF")

        return self.token(keyword or Tok.IDENTIFIER, identifier)

    def printstring(self, with_ln: bool = False):
        return self.token(
            Tok.PRINTSTRINGLN if with_ln else Tok.PRINTSTRING,
            "STRINGLN" if with_ln else "STRING",
        )

    def column(self):
        return self.start - self.line_start + 1

    def advance_while(self, condition):
        while condition(self.peek()) and not self.is_at_end():
            self.advance()

    def unexpected_character(self, char: str):
        return SyntaxError(
            f"Unexpected character: '{char}' at line {self.line}, column {self.column()}"
        )

    def operator(self):
        prev = self.previous()
        curr = self.peek()
        double_char = prev + curr
        if double_char in self.OPERATORS:
            self.advance()
            return self.token(self.OPERATORS[double_char], double_char)
        elif prev in self.OPERATORS:
            return self.token(self.OPERATORS[prev], prev)

        raise self.unexpected_character(curr)

    def skip_comment(self):
        self.advance_while(lambda c: c != "\n")
        if self.peek() == "\n":
            self.advance()
            self.eol()

    def skip_comment_block(self):
        while not self.match("END_REM"):
            self.skip_comment()

        if self.peek() == "\n":
            self.advance()
            self.eol()

    def token(self, tok: str, value: str = ""):
        return Token(tok, value, self.line, self.column())

    def eol(self):
        self.line += 1
        self.line_start = self.current
        return Token(Tok.EOL)

    def scan_token(self, previous: Token | None = None):
        char = self.advance()

        if char == "\n" and self.start == self.line_start:
            self.eol()  # Update line and line_start without yielding EOL
            return

        if char == "\n":
            return self.eol()
        elif previous and previous.type in {
            Tok.PRINTSTRING,
            Tok.PRINTSTRINGLN,
            Tok.RANDOM_CHAR_FROM,
        }:
            return self.string()
        elif previous and previous.type == Tok.RD_KBD:
            return self.kbd_platform()
        elif previous and previous.type == Tok.RD_KBD_PLATFORM:
            return self.kbd_language()
        elif self.is_operator(char):
            return self.operator()
        elif self.is_digit(char):
            return self.number()
        elif self.is_comment_block(char):
            return self.skip_comment_block()
        elif self.is_comment(char):
            return self.skip_comment()
        elif self.is_alpha(char):
            return self.identifier()
        elif char.isspace():
            return

        raise self.unexpected_character(char)
