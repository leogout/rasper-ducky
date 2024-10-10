import pytest
from lexer import (
    Lexer,
    TokenType,
    Token,
)  # Assurez-vous que ces imports correspondent à votre structure de projet


@pytest.fixture
def lexer():
    return Lexer()


def test_eof_token_empty_code(lexer):
    code = ""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [Token(TokenType.EOF, "", 1, 0)]
    assert tokens == expected_tokens


def test_eof_token_one_line_code(lexer):
    code = "VAR $x = 8"
    tokens = list(lexer.tokenize(code))
    assert tokens[-1] == Token(TokenType.EOF, "", 1, 10)


def test_eof_token_multiple_lines_code(lexer):
    code = """
    VAR $x = 8
    VAR $y = $x * 2 + 5
    """
    tokens = list(lexer.tokenize(code))
    assert tokens[-1] == Token(TokenType.EOF, "", 4, 4)


def test_eof_token_with_empty_lines(lexer):
    code = "\n\n\n\n\n\n"
    tokens = list(lexer.tokenize(code))
    assert tokens[-1] == Token(TokenType.EOF, "", 7, 0)


def test_var_declaration(lexer):
    code = "VAR $x = 8"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.VAR, "VAR", 1, 0),
        Token(TokenType.ID, "$x", 1, 4),
        Token(TokenType.ASSIGN, "=", 1, 7),
        Token(TokenType.NUMBER, "8", 1, 9),
        Token(TokenType.EOF, "", 1, 10),
    ]

    assert tokens == expected_tokens


def test_expression(lexer):
    code = "VAR $y = $x * 2 + 5"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.VAR, "VAR", 1, 0),
        Token(TokenType.ID, "$y", 1, 4),
        Token(TokenType.ASSIGN, "=", 1, 7),
        Token(TokenType.ID, "$x", 1, 9),
        Token(TokenType.OP, "*", 1, 12),
        Token(TokenType.NUMBER, "2", 1, 14),
        Token(TokenType.OP, "+", 1, 16),
        Token(TokenType.NUMBER, "5", 1, 18),
        Token(TokenType.EOF, "", 1, 19),
    ]
    assert tokens == expected_tokens


def test_string_statement(lexer):
    code = "STRING Hello, World!"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.PRINTSTRING, "STRING", 1, 0),
        Token(TokenType.STRING, "Hello, World!", 1, 8),
        Token(TokenType.EOF, "", 1, 20),
    ]
    assert tokens == expected_tokens


def test_all_keypress_commands(lexer):
    code = "\n".join(Lexer.COMMANDS)
    tokens = list(lexer.tokenize(code))

    expected_tokens = []
    for i, command in enumerate(Lexer.COMMANDS):
        expected_tokens.append(Token(TokenType.KEYPRESS, command, i + 1, 0))

    expected_tokens.append(
        Token(TokenType.EOF, "", len(Lexer.COMMANDS), len(Lexer.COMMANDS[-1]))
    )

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
        Token(TokenType.IF, "IF", 1, 0),
        Token(TokenType.NUMBER, "1", 1, 3),
        Token(TokenType.THEN, "THEN", 1, 5),
        Token(TokenType.PRINTSTRING, "STRING", 2, 0),
        Token(TokenType.STRING, "Hello, World!", 2, 8),
        Token(TokenType.ELSE_IF, "ELSE IF", 3, 0),
        Token(TokenType.NUMBER, "1", 3, 8),
        Token(TokenType.THEN, "THEN", 3, 10),
        Token(TokenType.PRINTSTRING, "STRING", 4, 0),
        Token(TokenType.STRING, "Hey ho!", 4, 8),
        Token(TokenType.ELSE, "ELSE", 5, 0),
        Token(TokenType.PRINTSTRING, "STRING", 6, 0),
        Token(TokenType.STRING, "Hey there!", 6, 8),
        Token(TokenType.END_IF, "END_IF", 7, 0),
        Token(TokenType.EOF, "", 8, 0),
    ]
    assert tokens == expected_tokens


def test_all_keywords_tokens(lexer):
    code = """STRING Hello, World!
VAR $x = 1 + 2 * 3 / 4 - 5 & 6 | 7 << 8 >> 9
VAR $y = 1 == 2 != 3 > 4 < 5 >= 6 <= 7 && 8 || 9
DELAY 10"""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.PRINTSTRING, "STRING", 1, 0),
        Token(TokenType.STRING, "Hello, World!", 1, 8),
        Token(TokenType.VAR, "VAR", 2, 0),
        Token(TokenType.ID, "$x", 2, 4),
        Token(TokenType.ASSIGN, "=", 2, 7),
        Token(TokenType.NUMBER, "1", 2, 9),
        Token(TokenType.OP, "+", 2, 11),
        Token(TokenType.NUMBER, "2", 2, 13),
        Token(TokenType.OP, "*", 2, 15),
        Token(TokenType.NUMBER, "3", 2, 17),
        Token(TokenType.OP, "/", 2, 19),
        Token(TokenType.NUMBER, "4", 2, 21),
        Token(TokenType.OP, "-", 2, 23),
        Token(TokenType.NUMBER, "5", 2, 25),
        Token(TokenType.OP, "&", 2, 27),
        Token(TokenType.NUMBER, "6", 2, 29),
        Token(TokenType.OP, "|", 2, 31),
        Token(TokenType.NUMBER, "7", 2, 33),
        Token(TokenType.OP, "<<", 2, 35),
        Token(TokenType.NUMBER, "8", 2, 38),
        Token(TokenType.OP, ">>", 2, 40),
        Token(TokenType.NUMBER, "9", 2, 43),
        Token(TokenType.VAR, "VAR", 3, 0),
        Token(TokenType.ID, "$y", 3, 4),
        Token(TokenType.ASSIGN, "=", 3, 7),
        Token(TokenType.NUMBER, "1", 3, 9),
        Token(TokenType.OP, "==", 3, 11),
        Token(TokenType.NUMBER, "2", 3, 14),
        Token(TokenType.OP, "!=", 3, 16),
        Token(TokenType.NUMBER, "3", 3, 19),
        Token(TokenType.OP, ">", 3, 21),
        Token(TokenType.NUMBER, "4", 3, 23),
        Token(TokenType.OP, "<", 3, 25),
        Token(TokenType.NUMBER, "5", 3, 27),
        Token(TokenType.OP, ">=", 3, 29),
        Token(TokenType.NUMBER, "6", 3, 32),
        Token(TokenType.OP, "<=", 3, 34),
        Token(TokenType.NUMBER, "7", 3, 37),
        Token(TokenType.OP, "&&", 3, 39),
        Token(TokenType.NUMBER, "8", 3, 42),
        Token(TokenType.OP, "||", 3, 44),
        Token(TokenType.NUMBER, "9", 3, 47),
        Token(TokenType.DELAY, "DELAY", 4, 0),
        Token(TokenType.NUMBER, "10", 4, 6),
        Token(TokenType.EOF, "", 4, 8),
    ]
    assert tokens == expected_tokens


def test_while_statement_with_expression(lexer):
    code = """WHILE ($x > 0)
STRING Hello, World!
$x = $x - 1
END_WHILE"""
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.WHILE, "WHILE", 1, 0),
        Token(TokenType.LPAREN, "(", 1, 6),
        Token(TokenType.ID, "$x", 1, 7),
        Token(TokenType.OP, ">", 1, 10),
        Token(TokenType.NUMBER, "0", 1, 12),
        Token(TokenType.RPAREN, ")", 1, 13),
        Token(TokenType.PRINTSTRING, "STRING", 2, 0),
        Token(TokenType.STRING, "Hello, World!", 2, 8),
        Token(TokenType.ID, "$x", 3, 0),
        Token(TokenType.ASSIGN, "=", 3, 3),
        Token(TokenType.ID, "$x", 3, 5),
        Token(TokenType.OP, "-", 3, 8),
        Token(TokenType.NUMBER, "1", 3, 10),
        Token(TokenType.END_WHILE, "END_WHILE", 4, 0),
        Token(TokenType.EOF, "", 4, 9),
    ]
    assert tokens == expected_tokens


def test_unexpected_character(lexer):
    code = "VAR $x = 8 @"
    with pytest.raises(
        SyntaxError, match=r"Unexpected character '@' at line 1, column 11"
    ):
        list(lexer.tokenize(code))


def test_invalid_operator(lexer):
    code = "VAR $x = 8 ^ 2"
    with pytest.raises(
        SyntaxError, match=r"Unexpected character '\^' at line 1, column 11"
    ):
        list(lexer.tokenize(code))


def test_invalid_keyword(lexer):
    code = "VOR $x = 8"
    with pytest.raises(
        SyntaxError, match=r"Unexpected character 'V' at line 1, column 0"
    ):
        list(lexer.tokenize(code))


def test_invalid_keyword_position(lexer):
    code = "VAR $x VAR"
    with pytest.raises(
        SyntaxError, match=r"Unexpected character 'V' at line 1, column 7"
    ):
        list(lexer.tokenize(code))
