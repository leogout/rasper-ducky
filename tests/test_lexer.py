import pytest
from lexer import *


@pytest.fixture
def lexer():
    return Lexer()


def test_eof_token_empty_code(lexer):
    code = ""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [Token(TokenType.EOF, "")]
    assert tokens == expected_tokens


def test_eof_token_one_line_code(lexer):
    code = "VAR $x = 8"
    tokens = list(lexer.tokenize(code))
    assert tokens[-1] == Token(TokenType.EOF, "")


def test_eof_token_multiple_lines_code(lexer):
    code = """
    VAR $x = 8
    VAR $y = $x * 2 + 5
    """
    tokens = list(lexer.tokenize(code))
    assert tokens[-1] == Token(TokenType.EOF, "")


def test_eof_token_with_empty_lines(lexer):
    code = "\n\n\n\n\n\n"
    tokens = list(lexer.tokenize(code))
    assert tokens[-1] == Token(TokenType.EOF, "")


def test_var_declaration(lexer):
    code = "VAR $x = 8"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.VAR, "VAR", 1, 1),
        Token(TokenType.IDENTIFIER, "$x", 1, 5),
        Token(TokenType.ASSIGN, "=", 1, 8),
        Token(TokenType.NUMBER, "8", 1, 10),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]

    assert tokens == expected_tokens


def test_expression(lexer):
    code = "VAR $y = $x * 2 + 5"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.VAR, "VAR", 1, 1),
        Token(TokenType.IDENTIFIER, "$y", 1, 5),
        Token(TokenType.ASSIGN, "=", 1, 8),
        Token(TokenType.IDENTIFIER, "$x", 1, 10),
        Token(TokenType.OP_MULTIPLY, "*", 1, 13),
        Token(TokenType.NUMBER, "2", 1, 15),
        Token(TokenType.OP_PLUS, "+", 1, 17),
        Token(TokenType.NUMBER, "5", 1, 19),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    assert tokens == expected_tokens


def test_string_statement(lexer):
    code = "STRING Hello, World!"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.PRINTSTRING, "STRING", 1, 1),
        Token(TokenType.STRING, "Hello, World!", 1, 9),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    assert tokens == expected_tokens


def test_stringln_statement(lexer):
    code = "STRINGLN Hello, World!"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.PRINTSTRINGLN, "STRINGLN", 1, 1),
        Token(TokenType.STRING, "Hello, World!", 1, 11),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    assert tokens == expected_tokens


def test_all_keypress_commands(lexer):
    code = "\n".join(Lexer.COMMANDS)
    tokens = list(lexer.tokenize(code))

    expected_tokens = []
    for i, command in enumerate(Lexer.COMMANDS):
        expected_tokens.append(Token(TokenType.KEYPRESS, command, i + 1, 1))
        expected_tokens.append(Token(TokenType.EOL, ""))
    expected_tokens.append(Token(TokenType.EOF, ""))

    assert tokens == expected_tokens


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
        Token(TokenType.IF, "IF", 1, 1),
        Token(TokenType.NUMBER, "1", 1, 4),
        Token(TokenType.THEN, "THEN", 1, 6),
        Token(TokenType.EOL, ""),
        Token(TokenType.PRINTSTRING, "STRING", 2, 1),
        Token(TokenType.STRING, "Hello, World!", 2, 9),
        Token(TokenType.EOL, ""),
        Token(TokenType.ELSE_IF, "ELSE IF", 3, 1),
        Token(TokenType.NUMBER, "1", 3, 9),
        Token(TokenType.THEN, "THEN", 3, 11),
        Token(TokenType.EOL, ""),
        Token(TokenType.PRINTSTRING, "STRING", 4, 1),
        Token(TokenType.STRING, "Hey ho!", 4, 9),
        Token(TokenType.EOL, ""),
        Token(TokenType.ELSE, "ELSE", 5, 1),
        Token(TokenType.EOL, ""),
        Token(TokenType.PRINTSTRING, "STRING", 6, 1),
        Token(TokenType.STRING, "Hey there!", 6, 9),
        Token(TokenType.EOL, ""),
        Token(TokenType.END_IF, "END_IF", 7, 1),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    assert tokens == expected_tokens


def test_all_keywords_tokens(lexer):
    code = """STRING Hello, World!
VAR $x = 1 + 2 * 3 / 4 - 5 & 6 | 7 << 8 >> 9
VAR $y = 1 == 2 != 3 > 4 < 5 >= 6 <= 7 && 8 || 9
DELAY 10"""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.PRINTSTRING, "STRING", 1, 1),
        Token(TokenType.STRING, "Hello, World!", 1, 9),
        Token(TokenType.EOL, ""),
        Token(TokenType.VAR, "VAR", 2, 1),
        Token(TokenType.IDENTIFIER, "$x", 2, 5),
        Token(TokenType.ASSIGN, "=", 2, 8),
        Token(TokenType.NUMBER, "1", 2, 10),
        Token(TokenType.OP_PLUS, "+", 2, 12),
        Token(TokenType.NUMBER, "2", 2, 14),
        Token(TokenType.OP_MULTIPLY, "*", 2, 16),
        Token(TokenType.NUMBER, "3", 2, 18),
        Token(TokenType.OP_DIVIDE, "/", 2, 20),
        Token(TokenType.NUMBER, "4", 2, 22),
        Token(TokenType.OP_MINUS, "-", 2, 24),
        Token(TokenType.NUMBER, "5", 2, 26),
        Token(TokenType.OP_BITWISE_AND, "&", 2, 28),
        Token(TokenType.NUMBER, "6", 2, 30),
        Token(TokenType.OP_BITWISE_OR, "|", 2, 32),
        Token(TokenType.NUMBER, "7", 2, 34),
        Token(TokenType.OP_SHIFT_LEFT, "<<", 2, 36),
        Token(TokenType.NUMBER, "8", 2, 39),
        Token(TokenType.OP_SHIFT_RIGHT, ">>", 2, 41),
        Token(TokenType.NUMBER, "9", 2, 44),
        Token(TokenType.EOL, ""),
        Token(TokenType.VAR, "VAR", 3, 1),
        Token(TokenType.IDENTIFIER, "$y", 3, 5),
        Token(TokenType.ASSIGN, "=", 3, 8),
        Token(TokenType.NUMBER, "1", 3, 10),
        Token(TokenType.OP_EQUAL, "==", 3, 12),
        Token(TokenType.NUMBER, "2", 3, 15),
        Token(TokenType.OP_NOT_EQUAL, "!=", 3, 17),
        Token(TokenType.NUMBER, "3", 3, 20),
        Token(TokenType.OP_GREATER, ">", 3, 22),
        Token(TokenType.NUMBER, "4", 3, 24),
        Token(TokenType.OP_LESS, "<", 3, 26),
        Token(TokenType.NUMBER, "5", 3, 28),
        Token(TokenType.OP_GREATER_EQUAL, ">=", 3, 30),
        Token(TokenType.NUMBER, "6", 3, 33),
        Token(TokenType.OP_LESS_EQUAL, "<=", 3, 35),
        Token(TokenType.NUMBER, "7", 3, 38),
        Token(TokenType.OP_AND, "&&", 3, 40),
        Token(TokenType.NUMBER, "8", 3, 43),
        Token(TokenType.OP_OR, "||", 3, 45),
        Token(TokenType.NUMBER, "9", 3, 48),
        Token(TokenType.EOL, ""),
        Token(TokenType.DELAY, "DELAY", 4, 1),
        Token(TokenType.NUMBER, "10", 4, 7),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    assert tokens == expected_tokens


def test_while_statement_with_expression(lexer):
    code = """WHILE ($x > 0)
STRING Hello, World!
$x = $x - 1
END_WHILE"""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.WHILE, "WHILE", 1, 1),
        Token(TokenType.LPAREN, "(", 1, 7),
        Token(TokenType.IDENTIFIER, "$x", 1, 8),
        Token(TokenType.OP_GREATER, ">", 1, 11),
        Token(TokenType.NUMBER, "0", 1, 13),
        Token(TokenType.RPAREN, ")", 1, 14),
        Token(TokenType.EOL, ""),
        Token(TokenType.PRINTSTRING, "STRING", 2, 1),
        Token(TokenType.STRING, "Hello, World!", 2, 9),
        Token(TokenType.EOL, ""),
        Token(TokenType.IDENTIFIER, "$x", 3, 1),
        Token(TokenType.ASSIGN, "=", 3, 4),
        Token(TokenType.IDENTIFIER, "$x", 3, 6),
        Token(TokenType.OP_MINUS, "-", 3, 9),
        Token(TokenType.NUMBER, "1", 3, 11),
        Token(TokenType.EOL, ""),
        Token(TokenType.END_WHILE, "END_WHILE", 4, 1),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    assert tokens == expected_tokens


def test_true_literal(lexer):
    code = "TRUE"
    tokens = list(lexer.tokenize(code))
    assert tokens == [
        Token(TokenType.TRUE, "TRUE", 1, 1),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]


def test_false_literal(lexer):
    code = "FALSE"
    tokens = list(lexer.tokenize(code))
    assert tokens == [
        Token(TokenType.FALSE, "FALSE", 1, 1),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
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


def test_invalid_keyword(lexer):
    code = "VOR $x = 8"
    with pytest.raises(
        SyntaxError, match=r"Unexpected character 'V' at line 1, column 1"
    ):
        list(lexer.tokenize(code))


def test_invalid_keyword_position(lexer):
    code = "VAR $x VAR"
    with pytest.raises(
        SyntaxError, match=r"Unexpected character 'V' at line 1, column 8"
    ):
        list(lexer.tokenize(code))
