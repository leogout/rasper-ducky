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
    NEWLINE = auto()
    SKIP = auto()
    MISMATCH = auto()
    PRINTSTRING = auto()
    STRING = auto()
    EOF = auto()
    KEYPRESS = auto()
    # for later

    # IF = auto()
    # THEN = auto()
    # ELSE = auto()
    # ELIF = auto()
    # END_IF = auto()

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
    line: int
    column: int





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
            (TokenType.VAR,           r'VAR'),
            (TokenType.DELAY,         r'DELAY'),
            (TokenType.KEYPRESS,      r'(?:^|\n)?' + '|'.join(re.escape(cmd) for cmd in self.COMMANDS) + r'(?:\n|$)'),
            (TokenType.PRINTSTRING,   r'STRING\s.*'),
            (TokenType.NEWLINE,       r'\n'),
            (TokenType.ID,            r'\$?[a-zA-Z_][a-zA-Z0-9_]*'),
            (TokenType.NUMBER,        r'\d+'),
            (TokenType.OP,            r'==|!=|>|<|>=|<=|&&|\|\||&|\||<<|>>|\+|\-|\*|/'),
            (TokenType.ASSIGN,        r'='),
            (TokenType.SKIP,          r'[ \t]+'),
            (TokenType.MISMATCH,      r'.'),
        ]
        self.token_regex = '|'.join('(?P<%s>%s)' % (t.name, r) for t, r in self.token_specification)

    def tokenize(self, code):
        line_num = 1
        line_start = 0
        for mo in re.finditer(self.token_regex, code):
            kind = TokenType[mo.lastgroup]
            value = mo.group()
            column = mo.start() - line_start
            if kind == TokenType.NEWLINE:
                if column > 0:  # Ignorer les lignes vides
                    yield Token(kind, value, line_num, column)
                line_start = mo.end()
                line_num += 1
            elif kind == TokenType.PRINTSTRING:
                yield Token(kind, value[:6], line_num, column)
                yield Token(TokenType.STRING, value[7:], line_num, 8)
            elif kind != TokenType.SKIP:
                yield Token(kind, value, line_num, column)
            elif kind == TokenType.KEYPRESS:
                yield Token(kind, value, line_num, 0)
        yield Token(TokenType.EOF, '', line_num, mo.end())