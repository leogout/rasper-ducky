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
    ]

    def __init__(self):
        self.token_specification = [
            (Tok.WAIT_FOR_BUTTON_PRESS, r"^\bWAIT_FOR_BUTTON_PRESS\b"),
            (Tok.REM, r"^\bREM\b.*"),
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
                r"\b(" + "|".join(re.escape(cmd) for cmd in self.COMMANDS) + r")\b",
            ),
            # Anything that is not a keyword is an identifier
            (Tok.REM_BLOCK, r"^\bREM_BLOCK\b.*"),
            (Tok.END_REM_BLOCK, r"^\bEND_REM\b"),
            (Tok.IDENTIFIER, r"\$?[a-zA-Z_][a-zA-Z0-9_]*"),
            (Tok.MISMATCH, r"."),
        ]
        self.token_regex = "|".join(
            f"(?P<{t.name}>{r})" for t, r in self.token_specification
        )

    def tokenize(self, code: str) -> Iterator[Token]:
        lines = code.split("\n")
        in_comment_block = False
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue

            if in_comment_block:
                if re.match(r"^\bEND_REM\b", line.strip()):
                    in_comment_block = False
                continue

            has_tokens = False
            for mo in re.finditer(self.token_regex, line.strip()):
                if mo.lastgroup is None:
                    raise SyntaxError(
                        f"Unexpected character '{mo.group()}' at line {line_num}, column {mo.start() + 1}"
                    )

                kind = Tok[mo.lastgroup]
                value = mo.group()
                column = mo.start() + 1
                if kind == Tok.MISMATCH:
                    raise SyntaxError(
                        f"Unexpected character '{value}' at line {line_num}, column {column}"
                    )
                elif kind == Tok.REM:
                    break
                elif kind == Tok.REM_BLOCK:
                    in_comment_block = True
                    break

                has_tokens = True
                if kind == Tok.PRINTSTRING:
                    yield Token(kind, "STRING", line_num, column)
                    yield Token(Tok.STRING, value[7:], line_num, column + 8)
                elif kind == Tok.PRINTSTRINGLN:
                    yield Token(kind, "STRINGLN", line_num, column)
                    yield Token(Tok.STRING, value[9:], line_num, column + 10)
                elif kind == Tok.KEYPRESS:
                    yield Token(kind, value.strip(), line_num, column)
                elif kind != Tok.SKIP:
                    yield Token(kind, value, line_num, column)

            if has_tokens:
                yield Token(Tok.EOL)

        yield Token(Tok.EOF)
