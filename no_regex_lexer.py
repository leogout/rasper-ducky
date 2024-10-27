from rasper_ducky.duckyscript.lexer import Token, Tok


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
    }

    KEYWORDS = {
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
        "WAIT_FOR_BUTTON_PRESS": Tok.WAIT_FOR_BUTTON_PRESS,
        "ATTACKMODE": Tok.ATTACKMODE,
        "HID": Tok.HID,
        "STORAGE": Tok.STORAGE,
        "OFF": Tok.OFF,

        "FUNCTION": Tok.FUNCTION,
        "END_FUNCTION": Tok.END_FUNCTION,
        "RETURN": Tok.RETURN,
        "TRUE": Tok.TRUE,
        "FALSE": Tok.FALSE,

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
        self.count = len(code)

    def is_at_end(self):
        return self.current >= self.count

    def advance(self):
        current = self.current
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self):
        if self.current > 0:
            return self.code[self.current - 1]
        return None

    def peek(self):
        if not self.is_at_end():
            return self.code[self.current]
        return None

    def peek_next(self):
        if self.current + 1 >= self.count:
            return None
        return self.code[self.current + 1]

    def match(self, expected: str):
        if self.is_at_end():
            return False

        original_position = self.current

        for char in expected:
            if self.peek() != char:
                self.current = original_position
                return False
            self.advance()

        return True

    def tokenize(self):
        while not self.is_at_end():
            self.start = self.current
            yield from self.scan_token()
        yield Token(Tok.EOL)
        yield Token(Tok.EOF)

    def is_digit(self, char: str):
        return char.isdigit()

    def is_alpha(self, char: str):
        return char.isalpha() or char == "$" or char == "_"

    def is_alphanumeric(self, char: str):
        return self.is_digit(char) or self.is_alpha(char)

    def is_operator(self, char: str):
        return char in "=><!&|^+-*/%^&|<>"

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        return self.token(Tok.NUMBER, float(self.code[self.start : self.current]))

    def string(self):
        start = self.current + 1
        while not self.is_at_end() and self.peek() != "\n":
            self.advance()
        return self.token(Tok.STRING, self.code[start : self.current])

    def identifier(self):
        while not self.is_at_end() and self.is_alphanumeric(self.peek()):
            self.advance()

        identifier = self.code[self.start : self.current]
        keyword = self.KEYWORDS.get(identifier)

        if keyword == Tok.ELSE and self.peek() == " ":
            while self.peek() == " ":
                self.advance()
            if self.match("IF"):
                return self.token(Tok.ELSE_IF)

        if keyword is not None:
            return self.token(keyword, identifier)

        return self.token(Tok.IDENTIFIER, identifier)

    def operator(self):
        prev = self.previous()
        curr = self.peek()
        double_char = prev + curr
        if double_char in self.OPERATORS:
            self.advance()
            return self.token(self.OPERATORS[double_char], double_char)
        elif prev in self.OPERATORS:
            return self.token(self.OPERATORS[prev], prev)
        
        raise Exception(f"Unexpected character: '{self.code[self.current - 1]}'")

    def token(self, tok: str, value: str = ""):
        return Token(tok, value, self.line, self.start - self.line_start + 1)

    def scan_token(self):
        char = self.advance()

        if self.is_operator(char):
            yield self.operator()
        elif char == "\n":
            self.line += 1
            self.line_start = self.current
            yield Token(Tok.EOL)
        elif self.is_digit(char):
            yield self.number()

        elif self.is_alpha(char):
            identifier = self.identifier()
            yield identifier
            self.start = self.current
            if identifier.type == Tok.PRINTSTRING or identifier.type == Tok.PRINTSTRINGLN:
                yield self.string()

        elif char == " ":
            pass
        else:
            raise Exception(f"Unexpected character: {char}")



if __name__ == "__main__":
    # lexer = Lexer("VAR $val = 10\nVAR $val2 = 20\n")
    # lexer = Lexer("CTRL A\nIF $val == 10 THEN\nELSE IF $val == 20 THEN\nEND_IF\n")
    # lexer = Lexer(' '.join(Lexer.OPERATORS.keys()))
    lexer = Lexer('STRING Hello, World!\nSTRINGLN Hello, World!')
    print(list(lexer.tokenize()))
