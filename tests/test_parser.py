import pytest
from parser import *
from lexer import *


@pytest.fixture
def parser():
    def _parser(tokens):
        return Parser(tokens)

    return _parser


def test_var_declaration(parser):
    tokens = [
        Token(TokenType.VAR, "VAR"),
        Token(TokenType.IDENTIFIER, "$x"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.NUMBER, "10"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [VarStmt(Token(TokenType.IDENTIFIER, "$x"), Literal("10"))]
    assert ast == expected_ast


def test_expression(parser):
    tokens = [
        Token(TokenType.VAR, "VAR"),
        Token(TokenType.IDENTIFIER, "$y"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.IDENTIFIER, "$x"),
        Token(TokenType.OP_MULTIPLY, "*"),
        Token(TokenType.NUMBER, "2"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$y"),
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_MULTIPLY, "*"),
                Literal("2"),
            ),
        )
    ]
    assert ast == expected_ast


def test_if_else_statement(parser):
    tokens = [
        Token(TokenType.IF, "IF"),
        Token(TokenType.IDENTIFIER, "$x"),
        Token(TokenType.OP_GREATER, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.THEN, "THEN"),
        Token(TokenType.EOL, ""),
        Token(TokenType.VAR, "VAR"),
        Token(TokenType.IDENTIFIER, "$y"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.NUMBER, "1"),
        Token(TokenType.EOL, ""),
        Token(TokenType.ELSE, "ELSE"),
        Token(TokenType.EOL, ""),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "Hey there!"),
        Token(TokenType.EOL, ""),
        Token(TokenType.END_IF, "END_IF"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        IfStmt(
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_GREATER, ">"),
                Literal("0"),
            ),
            [VarStmt(Token(TokenType.IDENTIFIER, "$y"), Literal("1"))],
            [],
            [StringStmt(Literal("Hey there!"))],
        )
    ]
    assert ast == expected_ast


def test_string_statement(parser):
    tokens = [
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "Hello, World!"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [StringStmt(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_stringln_statement(parser):
    tokens = [
        Token(TokenType.PRINTSTRINGLN, "STRINGLN"),
        Token(TokenType.STRING, "Hello, World!"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [StringLnStmt(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_if_else_if_else_statement(parser):
    tokens = [
        Token(TokenType.IF, "IF"),
        Token(TokenType.IDENTIFIER, "$x"),
        Token(TokenType.OP_GREATER, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.THEN, "THEN"),
        Token(TokenType.EOL, ""),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "A"),
        Token(TokenType.EOL, ""),
        Token(TokenType.ELSE_IF, "ELSE IF"),
        Token(TokenType.IDENTIFIER, "$x"),
        Token(TokenType.OP_LESS, "<"),
        Token(TokenType.NUMBER, "1"),
        Token(TokenType.THEN, "THEN"),
        Token(TokenType.EOL, ""),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "B"),
        Token(TokenType.EOL, ""),
        Token(TokenType.ELSE_IF, "ELSE IF"),
        Token(TokenType.IDENTIFIER, "$x"),
        Token(TokenType.OP_LESS, "<"),
        Token(TokenType.NUMBER, "1"),
        Token(TokenType.THEN, "THEN"),
        Token(TokenType.EOL, ""),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "C"),
        Token(TokenType.EOL, ""),
        Token(TokenType.ELSE, "ELSE"),
        Token(TokenType.EOL, ""),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "D"),
        Token(TokenType.EOL, ""),
        Token(TokenType.END_IF, "END_IF"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        IfStmt(
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_GREATER, ">"),
                Literal("0"),
            ),
            [StringStmt(Literal("A"))],
            [
                IfStmt(
                    Binary(
                        Variable(Token(TokenType.IDENTIFIER, "$x")),
                        Token(TokenType.OP_LESS, "<"),
                        Literal("1"),
                    ),
                    [StringStmt(Literal("B"))],
                ),
                IfStmt(
                    Binary(
                        Variable(Token(TokenType.IDENTIFIER, "$x")),
                        Token(TokenType.OP_LESS, "<"),
                        Literal("1"),
                    ),
                    [StringStmt(Literal("C"))],
                ),
            ],
            [StringStmt(Literal("D"))],
        )
    ]
    assert ast == expected_ast


def test_print_string(parser):
    tokens = [
        Token(TokenType.PRINTSTRING, "PRINTSTRING"),
        Token(TokenType.STRING, "Hello, World!"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [StringStmt(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_while_statement(parser):
    tokens = [
        Token(TokenType.WHILE, "WHILE"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.IDENTIFIER, "$x"),
        Token(TokenType.OP_GREATER, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.EOL, ""),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "Hello, World!"),
        Token(TokenType.EOL, ""),
        Token(TokenType.END_WHILE, "END_WHILE"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStmt(
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_GREATER, ">"),
                Literal("0"),
            ),
            [StringStmt(Literal("Hello, World!"))],
        )
    ]
    assert ast == expected_ast


def test_parentheses_priority_in_expression(parser):
    tokens = [
        Token(TokenType.VAR, "VAR"),
        Token(TokenType.IDENTIFIER, "$y"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.NUMBER, "3"),
        Token(TokenType.OP_MULTIPLY, "*"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.IDENTIFIER, "$x"),
        Token(TokenType.OP_PLUS, "+"),
        Token(TokenType.NUMBER, "2"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$y"),
            Binary(
                Literal("3"),
                Token(TokenType.OP_MULTIPLY, "*"),
                Binary(
                    Variable(Token(TokenType.IDENTIFIER, "$x")),
                    Token(TokenType.OP_PLUS, "+"),
                    Literal("2"),
                ),
            ),
        )
    ]
    assert ast == expected_ast


def test_parentheses_in_simple_expression(parser):
    tokens = [
        Token(TokenType.VAR, "VAR"),
        Token(TokenType.IDENTIFIER, "$y"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.NUMBER, "1"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [VarStmt(Token(TokenType.IDENTIFIER, "$y"), Literal("1"))]
    assert ast == expected_ast


def test_parentheses_in_while_statement(parser):
    tokens = [
        Token(TokenType.WHILE, "WHILE"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.IDENTIFIER, "$x"),
        Token(TokenType.OP_GREATER, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.EOL, ""),
        Token(TokenType.END_WHILE, "END_WHILE"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStmt(
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_GREATER, ">"),
                Literal("0"),
            ),
            [],
        )
    ]
    assert ast == expected_ast


def test_while_statement_with_number(parser):
    tokens = [
        Token(TokenType.WHILE, "WHILE"),
        Token(TokenType.NUMBER, "10"),
        Token(TokenType.EOL, ""),
        Token(TokenType.END_WHILE, "END_WHILE"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [WhileStmt(Literal("10"), [])]
    assert ast == expected_ast


def test_while_statement_without_parentheses(parser):
    tokens = [
        Token(TokenType.WHILE, "WHILE"),
        Token(TokenType.IDENTIFIER, "$x"),
        Token(TokenType.OP_GREATER, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.EOL, ""),
        Token(TokenType.END_WHILE, "END_WHILE"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStmt(
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_GREATER, ">"),
                Literal("0"),
            ),
            [],
        )
    ]
    assert ast == expected_ast


def test_literals(parser):
    tokens = [
        Token(TokenType.FALSE, "FALSE"),
        Token(TokenType.EOL, ""),
        Token(TokenType.TRUE, "TRUE"),
        Token(TokenType.EOL, ""),
        Token(TokenType.NUMBER, "10"),
        Token(TokenType.EOL, ""),
        Token(TokenType.STRING, "Hello, World!"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        ExpressionStmt(Literal(False)),
        ExpressionStmt(Literal(True)),
        ExpressionStmt(Literal("10")),
        ExpressionStmt(Literal("Hello, World!")),
    ]
    assert ast == expected_ast


def test_delay_statement(parser):
    tokens = [
        Token(TokenType.DELAY, "DELAY"),
        Token(TokenType.NUMBER, "10"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [DelayStmt(Literal("10"))]
    assert ast == expected_ast


def test_unary_expression(parser):
    tokens = [
        Token(TokenType.OP_MINUS, "-"),
        Token(TokenType.NUMBER, "10"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        ExpressionStmt(Unary(Token(TokenType.OP_MINUS, "-"), Literal("10")))
    ]
    assert ast == expected_ast
