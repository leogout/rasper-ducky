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


class Lexer:
    # WARNING: the order of the commands is important
    COMMANDS = [
        "WINDOWS",
        "GUI",
        "APP",
        "MENU",
        "SHIFT",
        "ALT",
        "CONTROL",
        "CTRL",
        "DOWNARROW",
        "DOWN",
        "LEFTARROW",
        "LEFT",
        "RIGHTARROW",
        "RIGHT",
        "UPARROW",
        "UP",
        "BREAK",
        "PAUSE",
        "CAPSLOCK",
        "DELETE",
        "END",
        "ESCAPE",
        "ESC",
        "HOME",
        "INSERT",
        "NUMLOCK",
        "PAGEUP",
        "PAGEDOWN",
        "PRINTSCREEN",
        "ENTER",
        "SCROLLLOCK",
        "SPACE",
        "TAB",
        "BACKSPACE",
        "F12",
        "F11",
        "F10",
        "F9",
        "F8",
        "F7",
        "F6",
        "F5",
        "F4",
        "F3",
        "F2",
        "F1",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]

    TOKEN_SPEC = [
        ("EOL", r"$"),
        ("WAIT_FOR_BUTTON_PRESS", r"^\bWAIT_FOR_BUTTON_PRESS\b"),
        ("ATTACKMODE", r"^\bATTACKMODE\b"),
        ("HID", r"\bHID\b"),
        ("STORAGE", r"\bSTORAGE\b"),
        ("OFF", r"\bOFF\b"),
        ("VAR", r"^\bVAR\b"),
        ("DELAY", r"^\bDELAY\b"),
        ("IF", r"^\bIF\b"),
        ("THEN", r"\bTHEN\b"),
        ("END_IF", r"^\bEND_IF\b"),
        ("ELSE_IF", r"^\bELSE\s+IF\b"),
        ("ELSE", r"^\bELSE\b"),
        ("PRINTSTRINGLN", r"^\bSTRINGLN\b\s.*"),
        ("PRINTSTRING", r"^\bSTRING\b\s.*"),
        ("TRUE", r"\bTRUE\b"),
        ("FALSE", r"\bFALSE\b"),
        ("WHILE", r"^\bWHILE\b"),
        ("END_WHILE", r"^\bEND_WHILE\b"),
        ("FUNCTION", r"^\bFUNCTION\b"),
        ("END_FUNCTION", r"^\bEND_FUNCTION\b"),
        ("NUMBER", r"\d+"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("OP_SHIFT_LEFT", r"<<"),
        ("OP_SHIFT_RIGHT", r">>"),
        ("OP_GREATER_EQUAL", r">="),
        ("OP_LESS_EQUAL", r"<="),
        ("OP_EQUAL", r"=="),
        ("OP_AND", r"&&"),
        ("OP_NOT_EQUAL", r"!="),
        ("OP_GREATER", r">"),
        ("OP_LESS", r"<"),
        ("OP_OR", r"\|\|"),
        ("OP_BITWISE_AND", r"&"),
        ("OP_BITWISE_OR", r"\|"),
        ("OP_PLUS", r"\+"),
        ("OP_MINUS", r"\-"),
        ("OP_MULTIPLY", r"\*"),
        ("OP_DIVIDE", r"/"),
        ("OP_MODULO", r"%"),
        ("OP_POWER", r"\^"),
        ("OP_NOT", r"!"),
        ("ASSIGN", r"="),
        ("SKIP", r"[ \t]+"),
        (
            "KEYPRESS",
            r"\b(" + "|".join(COMMANDS) + r")\b",
        ),
        # Anything that is not a keyword is an identifier
        ("IDENTIFIER", r"\$?[a-zA-Z_][a-zA-Z0-9_]*"),
        ("MISMATCH", r"."),
    ]

    def __init__(self, code: str):
        self.line_num = 1
        self.lines = code.splitlines()

    def advance(self):
        """Advance to the next line."""
        self.line_num += 1

    def get_line(self) -> str:
        """Get the current line."""
        return self.lines[self.line_num - 1]

    def skip_line(self, pattern: str) -> bool:
        """Skip a line if it matches the given pattern."""
        line = self.get_line()
        if re.match(pattern, line):
            self.advance()
            return True
        return False

    def skip_empty_line(self) -> bool:
        """Skip an empty line."""
        return self.skip_line(r"^\s*$")

    def skip_comment_line(self) -> bool:
        """Skip a comment line."""
        return self.skip_line(r"^\bREM\b")

    def skip_comment_block(self) -> bool:
        """Skip a block of comments."""
        if self.skip_line(r"^\bREM_BLOCK\b"):
            while not self.skip_line(r"^\bEND_REM\b"):
                self.advance()

            return True
        return False

    def consume_token(self, kind: str, value: str, column: int):
        """Consume a token and yield the appropriate Token object."""
        if kind == Tok.MISMATCH:
            raise SyntaxError(
                f"Unexpected character '{value}' at line {self.line_num}, column {column}"
            )
        elif kind == Tok.PRINTSTRING:
            yield Token(kind, "STRING", self.line_num, column)
            yield Token(Tok.STRING, value[7:].strip(), self.line_num, column + 8)
        elif kind == Tok.PRINTSTRINGLN:
            yield Token(kind, "STRINGLN", self.line_num, column)
            yield Token(Tok.STRING, value[9:].strip(), self.line_num, column + 10)
        elif kind == Tok.KEYPRESS:
            yield Token(kind, value.strip(), self.line_num, column)
        elif kind == Tok.EOL:
            yield Token(kind)
        elif kind != Tok.SKIP:
            yield Token(kind, value, self.line_num, column)

    def consume_line(self) -> Iterator[Token]:
        """Consume tokens from the current line."""
        line = self.get_line()
        column = 1

        while line:
            match_found = False
            for kind, pattern in self.TOKEN_SPEC:
                match = re.match(pattern, line)
                if match:
                    value = match.group(0)
                    match_found = True
                    line = line[len(value) :]  # Avance dans la ligne
                    yield from self.consume_token(kind, value, column)
                    column += len(value)
                    break

            if not match_found:
                raise SyntaxError(
                    f"Unrecognized token at line {self.line_num}, column {column}"
                )

            if not line:
                yield Token(Tok.EOL)

    def consume_line_no_regex(self) -> Iterator[Token]:
        """Consume tokens from the current line without using regex."""
        line = self.get_line()
        for command in self.COMMANDS:
            if line.startswith(command):
                yield Token(command)

    def tokenize(self) -> Iterator[Token]:
        """Tokenize the input code."""
        while self.line_num <= len(self.lines):
            if (
                self.skip_empty_line()
                or self.skip_comment_line()
                or self.skip_comment_block()
            ):
                continue

            yield from self.consume_line()
            self.advance()

        yield Token(Tok.EOF)
