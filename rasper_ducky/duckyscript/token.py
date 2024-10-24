from dataclasses import dataclass


class Tok:
    VAR = 0
    DELAY = 1
    IDENTIFIER = 2
    ASSIGN = 3
    SKIP = 4
    MISMATCH = 5
    PRINTSTRING = 6
    PRINTSTRINGLN = 7
    EOF = 8
    EOL = 9
    KEYPRESS = 10
    REM = 11
    REM_BLOCK = 12
    END_REM_BLOCK = 13

    WAIT_FOR_BUTTON_PRESS = 14
    ATTACKMODE = 15
    HID = 16
    STORAGE = 17
    OFF = 18

    IF = 19
    THEN = 20
    END_IF = 21
    ELSE = 22
    ELSE_IF = 23

    WHILE = 24
    END_WHILE = 25

    LPAREN = 26
    RPAREN = 27

    FUNCTION = 28
    END_FUNCTION = 29
    RETURN = 30

    # OPERATORS
    OP_SHIFT_LEFT = 31
    OP_SHIFT_RIGHT = 32
    OP_GREATER_EQUAL = 33
    OP_LESS_EQUAL = 34
    OP_EQUAL = 35
    OP_NOT_EQUAL = 36
    OP_GREATER = 37
    OP_LESS = 38
    OP_OR = 39
    OP_BITWISE_AND = 40
    OP_BITWISE_OR = 41
    OP_PLUS = 42
    OP_MINUS = 43
    OP_MULTIPLY = 44
    OP_DIVIDE = 45
    OP_MODULO = 46
    OP_POWER = 47
    OP_NOT = 48
    OP_AND = 49

    # LITERALS
    STRING = 50
    NUMBER = 51
    TRUE = 52
    FALSE = 53

    # Not in duckyscript 3.0 but why not implement it later
    # BREAK = auto()
    # CONTINUE = auto()


@dataclass
class Token:
    type: int
    value: str = ""
    line: int = 0
    column: int = 0
