import re
from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
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
    # REM = auto()
    # CONTINUE = auto()
    # FUNCTION = auto()
    # END_FUNCTION = auto()

    # Not in duckyscript 3.0 but why not implement it later
    # BREAK = auto()


@dataclass
class Token:
    type: TokenType
    value: str
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

    def __init__(self):
        self.token_specification = [
            (TokenType.VAR, r"^\bVAR\b"),
            (TokenType.DELAY, r"^\bDELAY\b"),
            (TokenType.IF, r"^\bIF\b"),
            (TokenType.THEN, r"\bTHEN\b"),
            (TokenType.END_IF, r"^\bEND_IF\b"),
            (TokenType.ELSE_IF, r"^\bELSE\s+IF\b"),
            (TokenType.ELSE, r"^\bELSE\b"),
            (TokenType.PRINTSTRINGLN, r"^\bSTRINGLN\b\s.*"),
            (TokenType.PRINTSTRING, r"^\bSTRING\b\s.*"),
            (TokenType.TRUE, r"\bTRUE\b"),
            (TokenType.FALSE, r"\bFALSE\b"),
            (TokenType.WHILE, r"^\bWHILE\b"),
            (TokenType.END_WHILE, r"^\bEND_WHILE\b"),
            (TokenType.IDENTIFIER, r"\$[a-zA-Z0-9_]+"),
            (TokenType.NUMBER, r"\d+"),
            (TokenType.LPAREN, r"\("),
            (TokenType.RPAREN, r"\)"),
            (TokenType.OP_SHIFT_LEFT, r"<<"),
            (TokenType.OP_SHIFT_RIGHT, r">>"),
            (TokenType.OP_GREATER_EQUAL, r">="),
            (TokenType.OP_LESS_EQUAL, r"<="),
            (TokenType.OP_EQUAL, r"=="),
            (TokenType.OP_AND, r"&&"),
            (TokenType.OP_NOT_EQUAL, r"!="),
            (TokenType.OP_GREATER, r">"),
            (TokenType.OP_LESS, r"<"),
            (TokenType.OP_OR, r"\|\|"),
            (TokenType.OP_BITWISE_AND, r"&"),
            (TokenType.OP_BITWISE_OR, r"\|"),
            (TokenType.OP_PLUS, r"\+"),
            (TokenType.OP_MINUS, r"\-"),
            (TokenType.OP_MULTIPLY, r"\*"),
            (TokenType.OP_DIVIDE, r"/"),
            (TokenType.OP_MODULO, r"%"),
            (TokenType.OP_POWER, r"\^"),
            (TokenType.OP_NOT, r"!"),
            (TokenType.ASSIGN, r"="),
            (TokenType.SKIP, r"[ \t]+"),
            (
                TokenType.KEYPRESS,
                r"\b(" + "|".join(re.escape(cmd) for cmd in self.COMMANDS) + r")\b",
            ),
            (TokenType.MISMATCH, r"."),
        ]
        self.token_regex = "|".join(
            "(?P<%s>%s)" % (t.name, r) for t, r in self.token_specification
        )

    def tokenize(self, code: str):
        lines = code.split("\n")
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            for mo in re.finditer(self.token_regex, line.strip()):
                if mo.lastgroup is None:
                    raise SyntaxError(
                        f"Unexpected character '{mo.group()}' at line {line_num}, column {mo.start() + 1}"
                    )
                kind = TokenType[mo.lastgroup]
                value = mo.group()
                column = mo.start() + 1
                if kind == TokenType.MISMATCH:
                    raise SyntaxError(
                        f"Unexpected character '{value}' at line {line_num}, column {column}"
                    )

                if kind == TokenType.PRINTSTRING:
                    yield Token(kind, "STRING", line_num, column)
                    yield Token(TokenType.STRING, value[7:], line_num, column + 8)
                elif kind == TokenType.PRINTSTRINGLN:
                    yield Token(kind, "STRINGLN", line_num, column)
                    yield Token(TokenType.STRING, value[9:], line_num, column + 10)
                elif kind == TokenType.KEYPRESS:
                    yield Token(kind, value.strip(), line_num, column)
                elif kind != TokenType.SKIP:
                    yield Token(kind, value, line_num, column)
            yield Token(TokenType.EOL, "")
        yield Token(TokenType.EOF, "")
