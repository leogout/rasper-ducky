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
        Token(Tok.VAR, "VAR"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.ASSIGN, "="),
        Token(Tok.NUMBER, "10"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [VarStmt(Token(Tok.IDENTIFIER, "$x"), Literal("10"))]
    assert ast == expected_ast


def test_expression(parser):
    tokens = [
        Token(Tok.VAR, "VAR"),
        Token(Tok.IDENTIFIER, "$y"),
        Token(Tok.ASSIGN, "="),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_MULTIPLY, "*"),
        Token(Tok.NUMBER, "2"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_MULTIPLY, "*"),
                Literal("2"),
            ),
        )
    ]
    assert ast == expected_ast


def test_if_else_statement(parser):
    tokens = [
        Token(Tok.IF, "IF"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_GREATER, ">"),
        Token(Tok.NUMBER, "0"),
        Token(Tok.THEN, "THEN"),
        Token(Tok.EOL),
        Token(Tok.VAR, "VAR"),
        Token(Tok.IDENTIFIER, "$y"),
        Token(Tok.ASSIGN, "="),
        Token(Tok.NUMBER, "1"),
        Token(Tok.EOL),
        Token(Tok.ELSE, "ELSE"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "Hey there!"),
        Token(Tok.EOL),
        Token(Tok.END_IF, "END_IF"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        IfStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_GREATER, ">"),
                Literal("0"),
            ),
            [VarStmt(Token(Tok.IDENTIFIER, "$y"), Literal("1"))],
            [],
            [StringStmt(Literal("Hey there!"))],
        )
    ]
    assert ast == expected_ast


def test_string_statement(parser):
    tokens = [
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "Hello, World!"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [StringStmt(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_stringln_statement(parser):
    tokens = [
        Token(Tok.PRINTSTRINGLN, "STRINGLN"),
        Token(Tok.STRING, "Hello, World!"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [StringLnStmt(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_if_else_if_else_statement(parser):
    tokens = [
        Token(Tok.IF, "IF"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_GREATER, ">"),
        Token(Tok.NUMBER, "0"),
        Token(Tok.THEN, "THEN"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "A"),
        Token(Tok.EOL),
        Token(Tok.ELSE_IF, "ELSE IF"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_LESS, "<"),
        Token(Tok.NUMBER, "1"),
        Token(Tok.THEN, "THEN"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "B"),
        Token(Tok.EOL),
        Token(Tok.ELSE_IF, "ELSE IF"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_LESS, "<"),
        Token(Tok.NUMBER, "1"),
        Token(Tok.THEN, "THEN"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "C"),
        Token(Tok.EOL),
        Token(Tok.ELSE, "ELSE"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "D"),
        Token(Tok.EOL),
        Token(Tok.END_IF, "END_IF"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        IfStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_GREATER, ">"),
                Literal("0"),
            ),
            [StringStmt(Literal("A"))],
            [
                IfStmt(
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$x")),
                        Token(Tok.OP_LESS, "<"),
                        Literal("1"),
                    ),
                    [StringStmt(Literal("B"))],
                ),
                IfStmt(
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$x")),
                        Token(Tok.OP_LESS, "<"),
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
        Token(Tok.PRINTSTRING, "PRINTSTRING"),
        Token(Tok.STRING, "Hello, World!"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [StringStmt(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_while_statement(parser):
    tokens = [
        Token(Tok.WHILE, "WHILE"),
        Token(Tok.LPAREN, "("),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_GREATER, ">"),
        Token(Tok.NUMBER, "0"),
        Token(Tok.RPAREN, ")"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "Hello, World!"),
        Token(Tok.EOL),
        Token(Tok.END_WHILE, "END_WHILE"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_GREATER, ">"),
                Literal("0"),
            ),
            [StringStmt(Literal("Hello, World!"))],
        )
    ]
    assert ast == expected_ast


def test_parentheses_priority_in_expression(parser):
    tokens = [
        Token(Tok.VAR, "VAR"),
        Token(Tok.IDENTIFIER, "$y"),
        Token(Tok.ASSIGN, "="),
        Token(Tok.NUMBER, "3"),
        Token(Tok.OP_MULTIPLY, "*"),
        Token(Tok.LPAREN, "("),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_PLUS, "+"),
        Token(Tok.NUMBER, "2"),
        Token(Tok.RPAREN, ")"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Binary(
                Literal("3"),
                Token(Tok.OP_MULTIPLY, "*"),
                Binary(
                    Variable(Token(Tok.IDENTIFIER, "$x")),
                    Token(Tok.OP_PLUS, "+"),
                    Literal("2"),
                ),
            ),
        )
    ]
    assert ast == expected_ast


def test_parentheses_in_simple_expression(parser):
    tokens = [
        Token(Tok.VAR, "VAR"),
        Token(Tok.IDENTIFIER, "$y"),
        Token(Tok.ASSIGN, "="),
        Token(Tok.LPAREN, "("),
        Token(Tok.NUMBER, "1"),
        Token(Tok.RPAREN, ")"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [VarStmt(Token(Tok.IDENTIFIER, "$y"), Literal("1"))]
    assert ast == expected_ast


def test_parentheses_in_while_statement(parser):
    tokens = [
        Token(Tok.WHILE, "WHILE"),
        Token(Tok.LPAREN, "("),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_GREATER, ">"),
        Token(Tok.NUMBER, "0"),
        Token(Tok.RPAREN, ")"),
        Token(Tok.EOL),
        Token(Tok.END_WHILE, "END_WHILE"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_GREATER, ">"),
                Literal("0"),
            ),
            [],
        )
    ]
    assert ast == expected_ast


def test_while_statement_with_number(parser):
    tokens = [
        Token(Tok.WHILE, "WHILE"),
        Token(Tok.NUMBER, "10"),
        Token(Tok.EOL),
        Token(Tok.END_WHILE, "END_WHILE"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [WhileStmt(Literal("10"), [])]
    assert ast == expected_ast


def test_while_statement_without_parentheses(parser):
    tokens = [
        Token(Tok.WHILE, "WHILE"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_GREATER, ">"),
        Token(Tok.NUMBER, "0"),
        Token(Tok.EOL),
        Token(Tok.END_WHILE, "END_WHILE"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_GREATER, ">"),
                Literal("0"),
            ),
            [],
        )
    ]
    assert ast == expected_ast


def test_literals(parser):
    tokens = [
        Token(Tok.FALSE, "FALSE"),
        Token(Tok.EOL),
        Token(Tok.TRUE, "TRUE"),
        Token(Tok.EOL),
        Token(Tok.NUMBER, "10"),
        Token(Tok.EOL),
        Token(Tok.STRING, "Hello, World!"),
        Token(Tok.EOL),
        Token(Tok.EOF),
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
        Token(Tok.DELAY, "DELAY"),
        Token(Tok.NUMBER, "10"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [DelayStmt(Literal("10"))]
    assert ast == expected_ast


def test_unary_expression(parser):
    tokens = [
        Token(Tok.OP_MINUS, "-"),
        Token(Tok.NUMBER, "10"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [ExpressionStmt(Unary(Token(Tok.OP_MINUS, "-"), Literal("10")))]
    assert ast == expected_ast
