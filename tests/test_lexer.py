import pytest
from rasper_ducky.duckyscript.lexer import *


@pytest.fixture
def lexer():
    return Lexer()


def test_eof_token_empty_code(lexer):
    code = ""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [Token(Tok.EOF)]
    assert tokens == expected_tokens


def test_eof_token_one_line_code(lexer):
    code = "VAR $x = 8"
    tokens = list(lexer.tokenize(code))
    assert tokens[-1] == Token(Tok.EOF)


def test_eof_token_multiple_lines_code(lexer):
    code = """
    VAR $x = 8
    VAR $y = $x * 2 + 5
    """
    tokens = list(lexer.tokenize(code))
    assert tokens[-1] == Token(Tok.EOF)


def test_eof_token_with_empty_lines(lexer):
    code = "\n\n\n\n\n\n"
    tokens = list(lexer.tokenize(code))
    assert tokens[-1] == Token(Tok.EOF)


def test_var_declaration(lexer):
    code = "VAR $x = 8"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.VAR, "VAR", 1, 1),
        Token(Tok.IDENTIFIER, "$x", 1, 5),
        Token(Tok.ASSIGN, "=", 1, 8),
        Token(Tok.NUMBER, "8", 1, 10),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]

    assert tokens == expected_tokens


def test_expression(lexer):
    code = "VAR $y = $x * 2 + 5"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.VAR, "VAR", 1, 1),
        Token(Tok.IDENTIFIER, "$y", 1, 5),
        Token(Tok.ASSIGN, "=", 1, 8),
        Token(Tok.IDENTIFIER, "$x", 1, 10),
        Token(Tok.OP_MULTIPLY, "*", 1, 13),
        Token(Tok.NUMBER, "2", 1, 15),
        Token(Tok.OP_PLUS, "+", 1, 17),
        Token(Tok.NUMBER, "5", 1, 19),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_string_statement(lexer):
    code = "STRING Hello, World!"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.PRINTSTRING, "STRING", 1, 1),
        Token(Tok.STRING, "Hello, World!", 1, 9),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_stringln_statement(lexer):
    code = "STRINGLN Hello, World!"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.PRINTSTRINGLN, "STRINGLN", 1, 1),
        Token(Tok.STRING, "Hello, World!", 1, 11),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_all_keypress_commands(lexer):
    code = "\n".join(Lexer.COMMANDS)
    tokens = list(lexer.tokenize(code))

    expected_tokens = []
    for i, command in enumerate(Lexer.COMMANDS):
        expected_tokens.append(Token(Tok.KEYPRESS, command, i + 1, 1))
        expected_tokens.append(Token(Tok.EOL))
    expected_tokens.append(Token(Tok.EOF))

    assert tokens == expected_tokens


def test_keypress_statement_with_multiple_keys(lexer):
    code = "A B"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.KEYPRESS, "A", 1, 10),
        Token(Tok.KEYPRESS, "B", 1, 12),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]


def test_if_else_statement(lexer):
    code = """IF 1 THEN
STRING Hello, World!
ELSE IF 1 THEN
STRING Hey ho!
ELSE
STRING Hey there!
END_IF
"""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.IF, "IF", 1, 1),
        Token(Tok.NUMBER, "1", 1, 4),
        Token(Tok.THEN, "THEN", 1, 6),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING", 2, 1),
        Token(Tok.STRING, "Hello, World!", 2, 9),
        Token(Tok.EOL),
        Token(Tok.ELSE_IF, "ELSE IF", 3, 1),
        Token(Tok.NUMBER, "1", 3, 9),
        Token(Tok.THEN, "THEN", 3, 11),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING", 4, 1),
        Token(Tok.STRING, "Hey ho!", 4, 9),
        Token(Tok.EOL),
        Token(Tok.ELSE, "ELSE", 5, 1),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING", 6, 1),
        Token(Tok.STRING, "Hey there!", 6, 9),
        Token(Tok.EOL),
        Token(Tok.END_IF, "END_IF", 7, 1),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_all_keywords_tokens(lexer):
    code = """STRING Hello, World!
VAR $x = 1 + 2 * 3 / 4 - 5 & 6 | 7 << 8 >> 9
VAR $y = 1 == 2 != 3 > 4 < 5 >= 6 <= 7 && 8 || 9
DELAY 10"""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.PRINTSTRING, "STRING", 1, 1),
        Token(Tok.STRING, "Hello, World!", 1, 9),
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
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_while_statement_with_expression(lexer):
    code = """WHILE ($x > 0)
STRING Hello, World!
$x = $x - 1
END_WHILE"""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.WHILE, "WHILE", 1, 1),
        Token(Tok.LPAREN, "(", 1, 7),
        Token(Tok.IDENTIFIER, "$x", 1, 8),
        Token(Tok.OP_GREATER, ">", 1, 11),
        Token(Tok.NUMBER, "0", 1, 13),
        Token(Tok.RPAREN, ")", 1, 14),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING", 2, 1),
        Token(Tok.STRING, "Hello, World!", 2, 9),
        Token(Tok.EOL),
        Token(Tok.IDENTIFIER, "$x", 3, 1),
        Token(Tok.ASSIGN, "=", 3, 4),
        Token(Tok.IDENTIFIER, "$x", 3, 6),
        Token(Tok.OP_MINUS, "-", 3, 9),
        Token(Tok.NUMBER, "1", 3, 11),
        Token(Tok.EOL),
        Token(Tok.END_WHILE, "END_WHILE", 4, 1),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_true_literal(lexer):
    code = "TRUE"
    tokens = list(lexer.tokenize(code))
    assert tokens == [
        Token(Tok.TRUE, "TRUE", 1, 1),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]


def test_false_literal(lexer):
    code = "FALSE"
    tokens = list(lexer.tokenize(code))
    assert tokens == [
        Token(Tok.FALSE, "FALSE", 1, 1),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]


def test_unexpected_character(lexer):
    code = "VAR $x = 8 @"
    with pytest.raises(
        SyntaxError, match=r"Unexpected character '@' at line 1, column 12"
    ):
        list(lexer.tokenize(code))


def test_invalid_operator(lexer):
    code = "VAR $x = 8 £ 2"
    with pytest.raises(
        SyntaxError, match=r"Unexpected character '£' at line 1, column 12"
    ):
        list(lexer.tokenize(code))


def test_comments(lexer):
    code = """
REM This is a comment
STRING Hello, World!
REM This is another comment
"""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.PRINTSTRING, "STRING", 3, 1),
        Token(Tok.STRING, "Hello, World!", 3, 9),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_comments_blocks(lexer):
    code = """
REM_BLOCK
STRING A
END_REM
STRING B
"""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.PRINTSTRING, "STRING", 5, 1),
        Token(Tok.STRING, "B", 5, 9),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_function_declaration(lexer):
    code = """FUNCTION MyFunction()
    STRING Hello, World!
END_FUNCTION"""
    tokens = list(lexer.tokenize(code))
    print(tokens)
    expected_tokens = [
        Token(Tok.FUNCTION, "FUNCTION", 1, 1),
        Token(Tok.IDENTIFIER, "MyFunction", 1, 10),
        Token(Tok.LPAREN, "(", 1, 20),
        Token(Tok.RPAREN, ")", 1, 21),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING", 2, 1),
        Token(Tok.STRING, "Hello, World!", 2, 9),
        Token(Tok.EOL),
        Token(Tok.END_FUNCTION, "END_FUNCTION", 3, 1),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_wait_for_button_press(lexer):
    code = "WAIT_FOR_BUTTON_PRESS"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.WAIT_FOR_BUTTON_PRESS, "WAIT_FOR_BUTTON_PRESS", 1, 1),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens


def test_attack_modes(lexer):
    code = "ATTACKMODE HID STORAGE"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(Tok.ATTACKMODE, "ATTACKMODE", 1, 1),
        Token(Tok.HID, "HID", 1, 12),
        Token(Tok.STORAGE, "STORAGE", 1, 16),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    assert tokens == expected_tokens
