import re
from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    VAR = auto()
    DELAY = auto()
    ID = auto()
    NUMBER = auto()
    OP = auto()
    ASSIGN = auto()
    SKIP = auto()
    MISMATCH = auto()
    PRINTSTRING = auto()
    STRING = auto()
    EOF = auto()
    KEYPRESS = auto()

    IF = auto()
    THEN = auto()
    END_IF = auto()
    ELSE = auto()
    ELSE_IF = auto()

    # WHILE = auto()
    # END_WHILE = auto()
    # LBREAK = auto()
    # CONTINUE = auto()
    # FUNCTION = auto()
    # END_FUNCTION = auto()
    # LPAREN = auto()
    # RPAREN = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int = 0
    column: int = 0

class Lexer:
    # WARNING: the order of the commands is important
    COMMANDS = [
        'WINDOWS', 'GUI', 'APP', 'MENU', 'SHIFT', 'ALT', 'CONTROL', 'CTRL',
        'DOWNARROW', 'DOWN', 'LEFTARROW', 'LEFT', 'RIGHTARROW', 'RIGHT',
        'UPARROW', 'UP', 'BREAK', 'PAUSE', 'CAPSLOCK', 'DELETE', 'END',
        'ESCAPE', 'ESC', 'HOME', 'INSERT', 'NUMLOCK', 'PAGEUP', 'PAGEDOWN',
        'PRINTSCREEN', 'ENTER', 'SCROLLLOCK', 'SPACE', 'TAB', 'BACKSPACE',
        'F12', 'F11', 'F10', 'F9', 'F8', 'F7', 'F6', 'F5', 'F4', 'F3', 'F2', 'F1',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    ]

    def __init__(self):
        self.token_specification = [
            (TokenType.VAR,           r'^\bVAR\b'),
            (TokenType.DELAY,         r'^\bDELAY\b'),
            (TokenType.IF,            r'^\bIF\b'),
            (TokenType.THEN,          r'\bTHEN\b'),
            (TokenType.END_IF,        r'^\bEND_IF\b'),
            (TokenType.ELSE_IF,       r'^\bELSE\s+IF\b'),
            (TokenType.ELSE,          r'^\bELSE\b'),
            (TokenType.PRINTSTRING,   r'^\bSTRING\b\s.*'),
            (TokenType.ID,            r'\$[a-zA-Z0-9_]+'),
            (TokenType.NUMBER,        r'\d+'),
            (TokenType.OP,            r'<<|>>|>=|<=|==|!=|>|<|&&|\|\||&|\||\+|\-|\*|/'),
            (TokenType.ASSIGN,        r'='),
            (TokenType.SKIP,          r'[ \t]+'),
            (TokenType.KEYPRESS,      r'\b(' + '|'.join(re.escape(cmd) for cmd in self.COMMANDS) + r')\b'),
            (TokenType.MISMATCH,      r'.'),
        ]
        self.token_regex = '|'.join('(?P<%s>%s)' % (t.name, r) for t, r in self.token_specification)

    def tokenize(self, code):
        lines = code.splitlines()
        for line_num, line in enumerate(lines, 1):
            for mo in re.finditer(self.token_regex, line.strip()):
                kind = TokenType[mo.lastgroup]
                value = mo.group()
                column = mo.start()
                if kind == TokenType.MISMATCH:
                    raise SyntaxError(f"Unexpected character '{value}' at line {line_num}, column {column}")
                    
                if kind == TokenType.PRINTSTRING:
                    yield Token(kind, 'STRING', line_num, column)
                    yield Token(TokenType.STRING, value[7:], line_num, column + 8)
                elif kind == TokenType.KEYPRESS:
                    yield Token(kind, value, line_num, column)
                elif kind != TokenType.SKIP:
                    yield Token(kind, value, line_num, column)         
        yield Token(TokenType.EOF, '', len(lines), len(line))
