import pytest
from rasper_ducky.duckyscript.lexer import (
    Lexer,
    Token,
    Tok,
)


def lexer(code: str):
    return Lexer(code)


def test_eof_token_empty_code():
    code = ""
    tokens = list(lexer(code).tokenize())
    expected_tokens = [Token(Tok.EOF)]
    assert tokens == expected_tokens


def test_eof_token_one_line_code():
    code = "VAR $x = 8"
    tokens = list(lexer(code).tokenize())
    assert tokens[-1] == Token(Tok.EOF)


def test_eof_token_multiple_lines_code():
    code = """
    VAR $x = 8
    VAR $y = $x * 2 + 5
    """
    tokens = list(lexer(code).tokenize())
    assert tokens[-1] == Token(Tok.EOF)


def test_skip_tabs():
    code = "\tVAR $x = 8"
    tokens = list(lexer(code).tokenize())
    assert tokens == [
        Token(Tok.VAR, "VAR", 1, 2),
        Token(Tok.IDENTIFIER, "$x", 1, 6),
        Token(Tok.ASSIGN, "=", 1, 9),
        Token(Tok.NUMBER, "8", 1, 11),
        Token(Tok.EOF),
    ]


def test_eof_token_with_empty_lines():
    code = "\n\n\n\n\n\n"
    tokens = list(lexer(code).tokenize())
    assert tokens[-1] == Token(Tok.EOF)


def test_var_declaration():
    code = "VAR $x = 8"
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.VAR, "VAR", 1, 1),
        Token(Tok.IDENTIFIER, "$x", 1, 5),
        Token(Tok.ASSIGN, "=", 1, 8),
        Token(Tok.NUMBER, "8", 1, 10),
        Token(Tok.EOF),
    ]

    assert tokens == expected_tokens


def test_expression():
    code = "VAR $y = $x * 2 + 5"
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.VAR, "VAR", 1, 1),
        Token(Tok.IDENTIFIER, "$y", 1, 5),
        Token(Tok.ASSIGN, "=", 1, 8),
        Token(Tok.IDENTIFIER, "$x", 1, 10),
        Token(Tok.OP_MULTIPLY, "*", 1, 13),
        Token(Tok.NUMBER, "2", 1, 15),
        Token(Tok.OP_PLUS, "+", 1, 17),
        Token(Tok.NUMBER, "5", 1, 19),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_string_statement():
    code = "STRING Hello, World!"
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.PRINTSTRING, "STRING", 1, 1),
        Token(Tok.STRING, "Hello, World!", 1, 8),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_stringln_statement():
    code = "STRINGLN Hello, World!"
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.PRINTSTRINGLN, "STRINGLN", 1, 1),
        Token(Tok.STRING, "Hello, World!", 1, 10),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_all_keypress_commands():
    keypress = [
        keypress for keypress, token in Lexer.KEYWORDS.items() if token == Tok.KEYPRESS
    ]
    code = "\n".join(keypress) + "\n"
    tokens = list(lexer(code).tokenize())

    expected_tokens = []
    for i, command in enumerate(keypress):
        expected_tokens.append(Token(Tok.KEYPRESS, command, i + 1, 1))
        expected_tokens.append(Token(Tok.EOL))
    expected_tokens.append(Token(Tok.EOF))

    assert tokens == expected_tokens


def test_if_else_statement():
    code = """IF 1 THEN
STRING Hello, World!
ELSE IF 1 THEN
STRING Hey ho!
ELSE
STRING Hey there!
END_IF
"""
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.IF, "IF", 1, 1),
        Token(Tok.NUMBER, "1", 1, 4),
        Token(Tok.THEN, "THEN", 1, 6),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING", 2, 1),
        Token(Tok.STRING, "Hello, World!", 2, 8),
        Token(Tok.EOL),
        Token(Tok.ELSE_IF, "ELSE IF", 3, 1),
        Token(Tok.NUMBER, "1", 3, 9),
        Token(Tok.THEN, "THEN", 3, 11),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING", 4, 1),
        Token(Tok.STRING, "Hey ho!", 4, 8),
        Token(Tok.EOL),
        Token(Tok.ELSE, "ELSE", 5, 1),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING", 6, 1),
        Token(Tok.STRING, "Hey there!", 6, 8),
        Token(Tok.EOL),
        Token(Tok.END_IF, "END_IF", 7, 1),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_all_keywords_tokens():
    code = """STRING Hello, World!
VAR $x = 1 + 2 * 3 / 4 - 5 & 6 | 7 << 8 >> 9
VAR $y = 1 == 2 != 3 > 4 < 5 >= 6 <= 7 && 8 || 9
DELAY 10"""
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.PRINTSTRING, "STRING", 1, 1),
        Token(Tok.STRING, "Hello, World!", 1, 8),
        Token(Tok.EOL),
        Token(Tok.VAR, "VAR", 2, 1),
        Token(Tok.IDENTIFIER, "$x", 2, 5),
        Token(Tok.ASSIGN, "=", 2, 8),
        Token(Tok.NUMBER, "1", 2, 10),
        Token(Tok.OP_PLUS, "+", 2, 12),
        Token(Tok.NUMBER, "2", 2, 14),
        Token(Tok.OP_MULTIPLY, "*", 2, 16),
        Token(Tok.NUMBER, "3", 2, 18),
        Token(Tok.OP_DIVIDE, "/", 2, 20),
        Token(Tok.NUMBER, "4", 2, 22),
        Token(Tok.OP_MINUS, "-", 2, 24),
        Token(Tok.NUMBER, "5", 2, 26),
        Token(Tok.OP_BITWISE_AND, "&", 2, 28),
        Token(Tok.NUMBER, "6", 2, 30),
        Token(Tok.OP_BITWISE_OR, "|", 2, 32),
        Token(Tok.NUMBER, "7", 2, 34),
        Token(Tok.OP_SHIFT_LEFT, "<<", 2, 36),
        Token(Tok.NUMBER, "8", 2, 39),
        Token(Tok.OP_SHIFT_RIGHT, ">>", 2, 41),
        Token(Tok.NUMBER, "9", 2, 44),
        Token(Tok.EOL),
        Token(Tok.VAR, "VAR", 3, 1),
        Token(Tok.IDENTIFIER, "$y", 3, 5),
        Token(Tok.ASSIGN, "=", 3, 8),
        Token(Tok.NUMBER, "1", 3, 10),
        Token(Tok.OP_EQUAL, "==", 3, 12),
        Token(Tok.NUMBER, "2", 3, 15),
        Token(Tok.OP_NOT_EQUAL, "!=", 3, 17),
        Token(Tok.NUMBER, "3", 3, 20),
        Token(Tok.OP_GREATER, ">", 3, 22),
        Token(Tok.NUMBER, "4", 3, 24),
        Token(Tok.OP_LESS, "<", 3, 26),
        Token(Tok.NUMBER, "5", 3, 28),
        Token(Tok.OP_GREATER_EQUAL, ">=", 3, 30),
        Token(Tok.NUMBER, "6", 3, 33),
        Token(Tok.OP_LESS_EQUAL, "<=", 3, 35),
        Token(Tok.NUMBER, "7", 3, 38),
        Token(Tok.OP_AND, "&&", 3, 40),
        Token(Tok.NUMBER, "8", 3, 43),
        Token(Tok.OP_OR, "||", 3, 45),
        Token(Tok.NUMBER, "9", 3, 48),
        Token(Tok.EOL),
        Token(Tok.DELAY, "DELAY", 4, 1),
        Token(Tok.NUMBER, "10", 4, 7),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_while_statement_with_expression():
    code = """WHILE ($x > 0)
STRING Hello, World!
$x = $x - 1
END_WHILE"""
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.WHILE, "WHILE", 1, 1),
        Token(Tok.LPAREN, "(", 1, 7),
        Token(Tok.IDENTIFIER, "$x", 1, 8),
        Token(Tok.OP_GREATER, ">", 1, 11),
        Token(Tok.NUMBER, "0", 1, 13),
        Token(Tok.RPAREN, ")", 1, 14),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING", 2, 1),
        Token(Tok.STRING, "Hello, World!", 2, 8),
        Token(Tok.EOL),
        Token(Tok.IDENTIFIER, "$x", 3, 1),
        Token(Tok.ASSIGN, "=", 3, 4),
        Token(Tok.IDENTIFIER, "$x", 3, 6),
        Token(Tok.OP_MINUS, "-", 3, 9),
        Token(Tok.NUMBER, "1", 3, 11),
        Token(Tok.EOL),
        Token(Tok.END_WHILE, "END_WHILE", 4, 1),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_true_literal():
    code = "TRUE"
    tokens = list(lexer(code).tokenize())
    assert tokens == [
        Token(Tok.TRUE, "TRUE", 1, 1),
        Token(Tok.EOF),
    ]


def test_false_literal():
    code = "FALSE"
    tokens = list(lexer(code).tokenize())
    assert tokens == [
        Token(Tok.FALSE, "FALSE", 1, 1),
        Token(Tok.EOF),
    ]


def test_unexpected_character():
    code = "VAR $x = 8 @"
    with pytest.raises(
        SyntaxError, match=r"Unexpected character: '@' at line 1, column 12"
    ):
        list(lexer(code).tokenize())


def test_invalid_operator():
    code = "VAR $x = 8 £ 2"
    with pytest.raises(
        SyntaxError, match=r"Unexpected character: '£' at line 1, column 12"
    ):
        list(lexer(code).tokenize())


def test_comments():
    code = """
REM This is a comment
STRING Hello, World!
REM This is another comment
"""
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.PRINTSTRING, "STRING", 3, 1),
        Token(Tok.STRING, "Hello, World!", 3, 8),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_comments_blocks():
    code = """REM_BLOCK
STRING A
END_REM
STRING B
"""
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.PRINTSTRING, "STRING", 4, 1),
        Token(Tok.STRING, "B", 4, 8),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_function_declaration():
    code = """FUNCTION MyFunction()
    STRING Hello, World!
END_FUNCTION"""
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.FUNCTION, "FUNCTION", 1, 1),
        Token(Tok.IDENTIFIER, "MyFunction", 1, 10),
        Token(Tok.LPAREN, "(", 1, 20),
        Token(Tok.RPAREN, ")", 1, 21),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING", 2, 5),
        Token(Tok.STRING, "Hello, World!", 2, 12),
        Token(Tok.EOL),
        Token(Tok.END_FUNCTION, "END_FUNCTION", 3, 1),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_attack_modes():
    code = "ATTACKMODE HID STORAGE"
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.ATTACKMODE, "ATTACKMODE", 1, 1),
        Token(Tok.HID, "HID", 1, 12),
        Token(Tok.STORAGE, "STORAGE", 1, 16),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_wait_for_button_press():
    code = "WAIT_FOR_BUTTON_PRESS"
    tokens = list(lexer(code).tokenize())
    expected_tokens = [
        Token(Tok.WAIT_FOR_BUTTON_PRESS, "WAIT_FOR_BUTTON_PRESS", 1, 1),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_trailing_spaces_ignored_after_print_commands():
    code = "STRING Hello, World!    "
    code += "\nSTRINGLN Hello, World!   "
    tokens = list(lexer(code).tokenize())
    assert tokens == [
        Token(Tok.PRINTSTRING, "STRING", 1, 1),
        Token(Tok.STRING, "Hello, World!", 1, 8),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRINGLN, "STRINGLN", 2, 1),
        Token(Tok.STRING, "Hello, World!", 2, 10),
        Token(Tok.EOF),
    ]


def test_kbd_commands():
    code = "RD_KBD WIN FR"
    tokens = list(lexer(code).tokenize())
    assert tokens == [
        Token(Tok.RD_KBD, "RD_KBD", 1, 1),
        Token(Tok.RD_KBD_PLATFORM, "WIN", 1, 8),
        Token(Tok.RD_KBD_LANGUAGE, "FR", 1, 12),
        Token(Tok.EOF),
    ]


def test_random_commands():
    code = """
RANDOM_LOWERCASE_LETTER
RANDOM_UPPERCASE_LETTER
RANDOM_LETTER
RANDOM_NUMBER
RANDOM_SPECIAL
RANDOM_CHAR
"""
    tokens = list(lexer(code).tokenize())
    assert tokens == [
        Token(Tok.RANDOM_CHAR, "RANDOM_LOWERCASE_LETTER", 2, 1),
        Token(Tok.EOL),
        Token(Tok.RANDOM_CHAR, "RANDOM_UPPERCASE_LETTER", 3, 1),
        Token(Tok.EOL),
        Token(Tok.RANDOM_CHAR, "RANDOM_LETTER", 4, 1),
        Token(Tok.EOL),
        Token(Tok.RANDOM_CHAR, "RANDOM_NUMBER", 5, 1),
        Token(Tok.EOL),
        Token(Tok.RANDOM_CHAR, "RANDOM_SPECIAL", 6, 1),
        Token(Tok.EOL),
        Token(Tok.RANDOM_CHAR, "RANDOM_CHAR", 7, 1),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]


def test_random_char_from():
    code = "RANDOM_CHAR_FROM aAzZ!#1,;:!()"
    tokens = list(lexer(code).tokenize())
    assert tokens == [
        Token(Tok.RANDOM_CHAR_FROM, "RANDOM_CHAR_FROM", 1, 1),
        Token(Tok.STRING, "aAzZ!#1,;:!()", 1, 18),
        Token(Tok.EOF),
    ]


def test_hold_release():
    code = """
HOLD A B C CTRL
RELEASE A B C CTRL
"""
    tokens = list(lexer(code).tokenize())
    assert tokens == [
        Token(Tok.HOLD, "HOLD", 2, 1),
        Token(Tok.KEYPRESS, "A", 2, 6),
        Token(Tok.KEYPRESS, "B", 2, 8),
        Token(Tok.KEYPRESS, "C", 2, 10),
        Token(Tok.KEYPRESS, "CTRL", 2, 12),
        Token(Tok.EOL),
        Token(Tok.RELEASE, "RELEASE", 3, 1),
        Token(Tok.KEYPRESS, "A", 3, 9),
        Token(Tok.KEYPRESS, "B", 3, 11),
        Token(Tok.KEYPRESS, "C", 3, 13),
        Token(Tok.KEYPRESS, "CTRL", 3, 15),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]


def test_double_char_operator_at_end_of_file():
    code = "add()"
    tokens = list(lexer(code).tokenize())
    assert tokens == [
        Token(Tok.IDENTIFIER, "add", 1, 1),
        Token(Tok.LPAREN, "(", 1, 4),
        Token(Tok.RPAREN, ")", 1, 5),
        Token(Tok.EOF),
    ]
