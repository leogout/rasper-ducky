import re

try:
    from typing import Iterator
except ImportError:
    pass


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
    # CONTINUE = "CONTINUE"

    # Not in duckyscript 3.0 but why not implement it later
    # BREAK = "BREAK"


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


# class Lexer:
#     # WARNING: the order of the commands is important
#     COMMANDS = [
#         "WINDOWS",
#         "GUI",
#         "APP",
#         "MENU",
#         "SHIFT",
#         "ALT",
#         "CONTROL",
#         "CTRL",
#         "DOWNARROW",
#         "DOWN",
#         "LEFTARROW",
#         "LEFT",
#         "RIGHTARROW",
#         "RIGHT",
#         "UPARROW",
#         "UP",
#         "BREAK",
#         "PAUSE",
#         "CAPSLOCK",
#         "DELETE",
#         "END",
#         "ESCAPE",
#         "ESC",
#         "HOME",
#         "INSERT",
#         "NUMLOCK",
#         "PAGEUP",
#         "PAGEDOWN",
#         "PRINTSCREEN",
#         "ENTER",
#         "SCROLLLOCK",
#         "SPACE",
#         "TAB",
#         "BACKSPACE",
#         "F12",
#         "F11",
#         "F10",
#         "F9",
#         "F8",
#         "F7",
#         "F6",
#         "F5",
#         "F4",
#         "F3",
#         "F2",
#         "F1",
#         "A",
#         "B",
#         "C",
#         "D",
#         "E",
#         "F",
#         "G",
#         "H",
#         "I",
#         "J",
#         "K",
#         "L",
#         "M",
#         "N",
#         "O",
#         "P",
#         "Q",
#         "R",
#         "S",
#         "T",
#         "U",
#         "V",
#         "W",
#         "X",
#         "Y",
#         "Z",
#     ]

#     TOKEN_SPEC = [
#         ("EOL", r"$"),
#         ("WAIT_FOR_BUTTON_PRESS", r"^\bWAIT_FOR_BUTTON_PRESS\b"),
#         ("ATTACKMODE", r"^\bATTACKMODE\b"),
#         ("HID", r"\bHID\b"),
#         ("STORAGE", r"\bSTORAGE\b"),
#         ("OFF", r"\bOFF\b"),
#         ("VAR", r"^\bVAR\b"),
#         ("DELAY", r"^\bDELAY\b"),
#         ("IF", r"^\bIF\b"),
#         ("THEN", r"\bTHEN\b"),
#         ("END_IF", r"^\bEND_IF\b"),
#         ("ELSE_IF", r"^\bELSE\s+IF\b"),
#         ("ELSE", r"^\bELSE\b"),
#         ("PRINTSTRINGLN", r"^\bSTRINGLN\b\s.*"),
#         ("PRINTSTRING", r"^\bSTRING\b\s.*"),
#         ("TRUE", r"\bTRUE\b"),
#         ("FALSE", r"\bFALSE\b"),
#         ("WHILE", r"^\bWHILE\b"),
#         ("END_WHILE", r"^\bEND_WHILE\b"),
#         ("FUNCTION", r"^\bFUNCTION\b"),
#         ("END_FUNCTION", r"^\bEND_FUNCTION\b"),
#         ("NUMBER", r"\d+"),
#         ("LPAREN", r"\("),
#         ("RPAREN", r"\)"),
#         ("OP_SHIFT_LEFT", r"<<"),
#         ("OP_SHIFT_RIGHT", r">>"),
#         ("OP_GREATER_EQUAL", r">="),
#         ("OP_LESS_EQUAL", r"<="),
#         ("OP_EQUAL", r"=="),
#         ("OP_AND", r"&&"),
#         ("OP_NOT_EQUAL", r"!="),
#         ("OP_GREATER", r">"),
#         ("OP_LESS", r"<"),
#         ("OP_OR", r"\|\|"),
#         ("OP_BITWISE_AND", r"&"),
#         ("OP_BITWISE_OR", r"\|"),
#         ("OP_PLUS", r"\+"),
#         ("OP_MINUS", r"\-"),
#         ("OP_MULTIPLY", r"\*"),
#         ("OP_DIVIDE", r"/"),
#         ("OP_MODULO", r"%"),
#         ("OP_POWER", r"\^"),
#         ("OP_NOT", r"!"),
#         ("ASSIGN", r"="),
#         ("SKIP", r"[ \t]+"),
#         (
#             "KEYPRESS",
#             r"\b(" + "|".join(COMMANDS) + r")\b",
#         ),
#         # Anything that is not a keyword is an identifier
#         ("IDENTIFIER", r"\$?[a-zA-Z_][a-zA-Z0-9_]*"),
#         ("MISMATCH", r"."),
#     ]

#     def __init__(self, code: str):
#         self.line_num = 1
#         self.lines = code.splitlines()

#     def advance(self):
#         """Advance to the next line."""
#         self.line_num += 1

#     def get_line(self) -> str:
#         """Get the current line."""
#         return self.lines[self.line_num - 1]

#     def skip_line(self, pattern: str) -> bool:
#         """Skip a line if it matches the given pattern."""
#         line = self.get_line()
#         if re.match(pattern, line):
#             self.advance()
#             return True
#         return False

#     def skip_empty_line(self) -> bool:
#         """Skip an empty line."""
#         return self.skip_line(r"^\s*$")

#     def skip_comment_line(self) -> bool:
#         """Skip a comment line."""
#         return self.skip_line(r"^\bREM\b")

#     def skip_comment_block(self) -> bool:
#         """Skip a block of comments."""
#         if self.skip_line(r"^\bREM_BLOCK\b"):
#             while not self.skip_line(r"^\bEND_REM\b"):
#                 self.advance()

#             return True
#         return False

#     def consume_token(self, kind: str, value: str, column: int):
#         """Consume a token and yield the appropriate Token object."""
#         if kind == Tok.MISMATCH:
#             raise SyntaxError(
#                 f"Unexpected character '{value}' at line {self.line_num}, column {column}"
#             )
#         elif kind == Tok.PRINTSTRING:
#             yield Token(kind, "STRING", self.line_num, column)
#             yield Token(Tok.STRING, value[7:].strip(), self.line_num, column + 8)
#         elif kind == Tok.PRINTSTRINGLN:
#             yield Token(kind, "STRINGLN", self.line_num, column)
#             yield Token(Tok.STRING, value[9:].strip(), self.line_num, column + 10)
#         elif kind == Tok.KEYPRESS:
#             yield Token(kind, value.strip(), self.line_num, column)
#         elif kind == Tok.EOL:
#             yield Token(kind)
#         elif kind != Tok.SKIP:
#             yield Token(kind, value, self.line_num, column)

#     def consume_line(self) -> Iterator[Token]:
#         """Consume tokens from the current line."""
#         line = self.get_line()
#         column = 1

#         while line:
#             match_found = False
#             for kind, pattern in self.TOKEN_SPEC:
#                 match = re.match(pattern, line)
#                 if match:
#                     value = match.group(0)
#                     match_found = True
#                     line = line[len(value) :]  # Avance dans la ligne
#                     yield from self.consume_token(kind, value, column)
#                     column += len(value)
#                     break

#             if not match_found:
#                 raise SyntaxError(
#                     f"Unrecognized token at line {self.line_num}, column {column}"
#                 )

#             if not line:
#                 yield Token(Tok.EOL)

#     def consume_line_no_regex(self) -> Iterator[Token]:
#         """Consume tokens from the current line without using regex."""
#         line = self.get_line()
#         for command in self.COMMANDS:
#             if line.startswith(command):
#                 yield Token(command)

#     def tokenize(self) -> Iterator[Token]:
#         """Tokenize the input code."""
#         while self.line_num <= len(self.lines):
#             if (
#                 self.skip_empty_line()
#                 or self.skip_comment_line()
#                 or self.skip_comment_block()
#             ):
#                 continue

#             yield from self.consume_line()
#             self.advance()

#         yield Token(Tok.EOF)
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
        return char in "=><!&|^+-*/%^&|<>()"

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        return self.token(Tok.NUMBER, float(self.code[self.start : self.current]))

    def string(self):
        while not self.is_at_end() and self.peek() != "\n":
            self.advance()
        return self.token(Tok.STRING, self.code[self.start : self.current].strip())

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
        return Token(tok, value, self.line, (self.start - self.line_start) + 1)

    def eol(self):
        self.line += 1
        self.line_start = self.current
        yield Token(Tok.EOL)

    def scan_token(self):
        char = self.advance()

        if self.is_operator(char):
            yield self.operator()
        elif char == "\n":
            yield self.eol()
        elif self.is_digit(char):
            yield self.number()

        elif self.is_alpha(char):
            identifier = self.identifier()
            yield identifier
            if identifier.type == Tok.PRINTSTRING or identifier.type == Tok.PRINTSTRINGLN:
                self.advance()
                self.start = self.current
                yield self.string()

        elif char == " ":
            pass
        else:
            raise Exception(f"Unexpected character: {char}")
