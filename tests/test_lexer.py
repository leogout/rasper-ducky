import pytest
from lexer import Lexer, TokenType, Token  # Assurez-vous que ces imports correspondent à votre structure de projet

@pytest.fixture
def lexer():
    return Lexer()

def test_var_declaration(lexer):
    code = "VAR $x = MAX_VALUE"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.VAR, 'VAR', 1, 0),
        Token(TokenType.ID, '$x', 1, 4),
        Token(TokenType.ASSIGN, '=', 1, 7),
        Token(TokenType.ID, 'MAX_VALUE', 1, 9),
        Token(TokenType.EOF, '', 1, 18)
    ]

    assert tokens == expected_tokens

def test_expression(lexer):
    code = "VAR $y = $x * 2 + 5"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.VAR, 'VAR', 1, 0),
        Token(TokenType.ID, '$y', 1, 4),
        Token(TokenType.ASSIGN, '=', 1, 7),
        Token(TokenType.ID, '$x', 1, 9),
        Token(TokenType.OP, '*', 1, 12),
        Token(TokenType.NUMBER, '2', 1, 14),
        Token(TokenType.OP, '+', 1, 16),
        Token(TokenType.NUMBER, '5', 1, 18),
        Token(TokenType.EOF, '', 1, 19)
    ]
    assert tokens == expected_tokens

def test_string_statement(lexer):
    code = "STRING Hello, World!"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.PRINTSTRING, 'STRING', 1, 0),
        Token(TokenType.STRING, 'Hello, World!', 1, 8),
        Token(TokenType.EOF, '', 1, 20)
    ]
    assert tokens == expected_tokens

def test_var_assignment(lexer):
    code = "VAR $spam = 5"
    tokens = list(lexer.tokenize(code))
    expected_tokens = [
        Token(TokenType.VAR, 'VAR', 1, 0),
        Token(TokenType.ID, '$spam', 1, 4),
        Token(TokenType.ASSIGN, '=', 1, 10),
        Token(TokenType.NUMBER, '5', 1, 12),
        Token(TokenType.EOF, '', 1, 13)
    ]
    
    assert tokens == expected_tokens

def test_keypress_command(lexer):
    code = '\n'.join(Lexer.COMMANDS) + '\n'
    tokens = list(lexer.tokenize(code))

    expected_tokens = [
        Token(TokenType.KEYPRESS, command, i + 1, 0) for i, command in enumerate(Lexer.COMMANDS)
    ]
    expected_tokens.append(Token(TokenType.EOF, '', len(Lexer.COMMANDS) + 1, 0))

    assert tokens == expected_tokens
    
