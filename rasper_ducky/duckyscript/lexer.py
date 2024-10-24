import re
from typing import Iterator

from .token import Token, Tok


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
        self.token_specification = {
            "ATTACKMODE": r"^\bATTACKMODE\b",
            "HID": r"\bHID\b",
            "STORAGE": r"\bSTORAGE\b",
            "OFF": r"\bOFF\b",
            "WAIT_FOR_BUTTON_PRESS": r"^\bWAIT_FOR_BUTTON_PRESS\b",
            "REM": r"^\bREM\b.*",
            "VAR": r"^\bVAR\b",
            "DELAY": r"^\bDELAY\b",
            "IF": r"^\bIF\b",
            "THEN": r"\bTHEN\b",
            "END_IF": r"^\bEND_IF\b",
            "ELSE_IF": r"^\bELSE\s+IF\b",
            "ELSE": r"^\bELSE\b",
            "PRINTSTRINGLN": r"^\bSTRINGLN\b\s.*",
            "PRINTSTRING": r"^\bSTRING\b\s.*",
            "TRUE": r"\bTRUE\b",
            "FALSE": r"\bFALSE\b",
            "WHILE": r"^\bWHILE\b",
            "END_WHILE": r"^\bEND_WHILE\b",
            "FUNCTION": r"^\bFUNCTION\b",
            "END_FUNCTION": r"^\bEND_FUNCTION\b",
            "NUMBER": r"\d+",
            "LPAREN": r"\(",
            "RPAREN": r"\)",
            "OP_SHIFT_LEFT": r"<<",
            "OP_SHIFT_RIGHT": r">>",
            "OP_GREATER_EQUAL": r">=",
            "OP_LESS_EQUAL": r"<=",
            "OP_EQUAL": r"==",
            "OP_AND": r"&&",
            "OP_NOT_EQUAL": r"!=",
            "OP_GREATER": r">",
            "OP_LESS": r"<",
            "OP_OR": r"\|\|",
            "OP_BITWISE_AND": r"&",
            "OP_BITWISE_OR": r"\|",
            "OP_PLUS": r"\+",
            "OP_MINUS": r"\-",
            "OP_MULTIPLY": r"\*",
            "OP_DIVIDE": r"/",
            "OP_MODULO": r"%",
            "OP_POWER": r"\^",
            "OP_NOT": r"!",
            "ASSIGN": r"=",
            "SKIP": r"[ \t]+",
            "KEYPRESS": r"\b("
            + "|".join(re.escape(cmd) for cmd in self.COMMANDS)
            + r")\b",
            "REM_BLOCK": r"^\bREM_BLOCK\b.*",
            "END_REM_BLOCK": r"^\bEND_REM\b",
            "IDENTIFIER": r"\$?[a-zA-Z_][a-zA-Z0-9_]*",
            "MISMATCH": r".",
        }
        self.token_regex = "|".join(
            f"(?P<{t}>{r})" for t, r in self.token_specification.items()
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

                kind = getattr(Tok, mo.lastgroup)
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
