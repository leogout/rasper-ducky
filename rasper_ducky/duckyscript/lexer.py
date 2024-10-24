import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import Iterator


class Tok(Enum):
    VAR = auto()
    DELAY = auto()
    IDENTIFIER = auto()
    ASSIGN = auto()
    SKIP = auto()
    MISMATCH = auto()
    PRINTSTRING = auto()
    PRINTSTRINGLN = auto()
    EOF = auto()
    EOL = auto()
    KEYPRESS = auto()
    REM = auto()
    REM_BLOCK = auto()
    END_REM_BLOCK = auto()

    WAIT_FOR_BUTTON_PRESS = auto()

    ATTACKMODE = auto()
    HID = auto()
    STORAGE = auto()
    OFF = auto()

    IF = auto()
    THEN = auto()
    END_IF = auto()
    ELSE = auto()
    ELSE_IF = auto()

    WHILE = auto()
    END_WHILE = auto()

    LPAREN = auto()
    RPAREN = auto()

    FUNCTION = auto()
    END_FUNCTION = auto()
    RETURN = auto()

    # OPERATORS
    OP_SHIFT_LEFT = auto()
    OP_SHIFT_RIGHT = auto()
    OP_GREATER_EQUAL = auto()
    OP_LESS_EQUAL = auto()
    OP_EQUAL = auto()
    OP_NOT_EQUAL = auto()
    OP_GREATER = auto()
    OP_LESS = auto()
    OP_OR = auto()
    OP_BITWISE_AND = auto()
    OP_BITWISE_OR = auto()
    OP_PLUS = auto()
    OP_MINUS = auto()
    OP_MULTIPLY = auto()
    OP_DIVIDE = auto()
    OP_MODULO = auto()
    OP_POWER = auto()
    OP_NOT = auto()
    OP_AND = auto()

    # LITERALS
    STRING = auto()
    NUMBER = auto()
    TRUE = auto()
    FALSE = auto()
    # CONTINUE = auto()

    # Not in duckyscript 3.0 but why not implement it later
    # BREAK = auto()


@dataclass
class Token:
    type: Tok
    value: str = ""
    line: int = 0
    column: int = 0


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
        (Tok.EOL, r"$"),
        (Tok.WAIT_FOR_BUTTON_PRESS, r"^\bWAIT_FOR_BUTTON_PRESS\b"),
        (Tok.ATTACKMODE, r"^\bATTACKMODE\b"),
        (Tok.HID, r"\bHID\b"),
        (Tok.STORAGE, r"\bSTORAGE\b"),
        (Tok.OFF, r"\bOFF\b"),
        (Tok.VAR, r"^\bVAR\b"),
        (Tok.DELAY, r"^\bDELAY\b"),
        (Tok.IF, r"^\bIF\b"),
        (Tok.THEN, r"\bTHEN\b"),
        (Tok.END_IF, r"^\bEND_IF\b"),
        (Tok.ELSE_IF, r"^\bELSE\s+IF\b"),
        (Tok.ELSE, r"^\bELSE\b"),
        (Tok.PRINTSTRINGLN, r"^\bSTRINGLN\b\s.*"),
        (Tok.PRINTSTRING, r"^\bSTRING\b\s.*"),
        (Tok.TRUE, r"\bTRUE\b"),
        (Tok.FALSE, r"\bFALSE\b"),
        (Tok.WHILE, r"^\bWHILE\b"),
        (Tok.END_WHILE, r"^\bEND_WHILE\b"),
        (Tok.FUNCTION, r"^\bFUNCTION\b"),
        (Tok.END_FUNCTION, r"^\bEND_FUNCTION\b"),
        (Tok.NUMBER, r"\d+"),
        (Tok.LPAREN, r"\("),
        (Tok.RPAREN, r"\)"),
        (Tok.OP_SHIFT_LEFT, r"<<"),
        (Tok.OP_SHIFT_RIGHT, r">>"),
        (Tok.OP_GREATER_EQUAL, r">="),
        (Tok.OP_LESS_EQUAL, r"<="),
        (Tok.OP_EQUAL, r"=="),
        (Tok.OP_AND, r"&&"),
        (Tok.OP_NOT_EQUAL, r"!="),
        (Tok.OP_GREATER, r">"),
        (Tok.OP_LESS, r"<"),
        (Tok.OP_OR, r"\|\|"),
        (Tok.OP_BITWISE_AND, r"&"),
        (Tok.OP_BITWISE_OR, r"\|"),
        (Tok.OP_PLUS, r"\+"),
        (Tok.OP_MINUS, r"\-"),
        (Tok.OP_MULTIPLY, r"\*"),
        (Tok.OP_DIVIDE, r"/"),
        (Tok.OP_MODULO, r"%"),
        (Tok.OP_POWER, r"\^"),
        (Tok.OP_NOT, r"!"),
        (Tok.ASSIGN, r"="),
        (Tok.SKIP, r"[ \t]+"),
        (
            Tok.KEYPRESS,
            r"\b(" + "|".join(re.escape(cmd) for cmd in COMMANDS) + r")\b",
        ),
        # Anything that is not a keyword is an identifier
        (Tok.IDENTIFIER, r"\$?[a-zA-Z_][a-zA-Z0-9_]*"),
        (Tok.MISMATCH, r"."),
    ]

    TOKEN_REGEX = "|".join(f"(?P<{t.name}>{r})" for t, r in TOKEN_SPEC)

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

    def consume_token(self, kind: Tok, value: str, column: int):
        """Consume a token and yield the appropriate Token object."""
        match kind:
            case Tok.MISMATCH:
                raise SyntaxError(
                    f"Unexpected character '{value}' at line {self.line_num}, column {column}"
                )
            case Tok.PRINTSTRING:
                yield Token(kind, "STRING", self.line_num, column)
                yield Token(Tok.STRING, value[7:], self.line_num, column + 8)
            case Tok.PRINTSTRINGLN:
                yield Token(kind, "STRINGLN", self.line_num, column)
                yield Token(Tok.STRING, value[9:], self.line_num, column + 10)
            case Tok.KEYPRESS:
                yield Token(kind, value.strip(), self.line_num, column)
            case Tok.EOL:
                yield Token(kind)
            case _ if kind != Tok.SKIP:
                yield Token(kind, value, self.line_num, column)

    def consume_line(self) -> Iterator[Token]:
        """Consume tokens from the current line."""
        line = self.get_line()
        for mo in re.finditer(self.TOKEN_REGEX, line.strip()):
            if mo.lastgroup is None:
                raise SyntaxError(
                    f"Unrecognized token '{mo.group()}' at line {self.line_num}, column {mo.start() + 1}"
                )

            kind = Tok[mo.lastgroup]
            value = mo.group()
            column = mo.start() + 1

            yield from self.consume_token(kind, value, column)

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
