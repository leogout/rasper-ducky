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
        Token(TokenType.ID, "$x"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.NUMBER, "10"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [VarDeclarationNode("$x", Literal("10"))]
    assert ast == expected_ast


def test_expression(parser):
    tokens = [
        Token(TokenType.VAR, "VAR"),
        Token(TokenType.ID, "$y"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP_MULTIPLY, "*"),
        Token(TokenType.NUMBER, "2"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarDeclarationNode(
            "$y",
            Binary(VarNode("$x"), Token(TokenType.OP_MULTIPLY, "*"), Literal("2")),
        )
    ]
    assert ast == expected_ast


def test_if_else_statement(parser):
    tokens = [
        Token(TokenType.IF, "IF"),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP_GREATER, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.THEN, "THEN"),
        Token(TokenType.VAR, "VAR"),
        Token(TokenType.ID, "$y"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.NUMBER, "1"),
        Token(TokenType.ELSE, "ELSE"),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "Hey there!"),
        Token(TokenType.END_IF, "END_IF"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        IfStatementNode(
            Binary(VarNode("$x"), Token(TokenType.OP_GREATER, ">"), Literal("0")),
            [VarDeclarationNode("$y", Literal("1"))],
            [],
            [PrintStringNode(Literal("Hey there!"))],
        )
    ]
    assert ast == expected_ast


def test_string_statement(parser):
    tokens = [
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "Hello, World!"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [PrintStringNode(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_stringln_statement(parser):
    tokens = [
        Token(TokenType.PRINTSTRINGLN, "STRINGLN"),
        Token(TokenType.STRING, "Hello, World!"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [PrintStringLnNode(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_if_else_if_else_statement(parser):
    tokens = [
        Token(TokenType.IF, "IF"),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP_GREATER, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.THEN, "THEN"),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "A"),
        Token(TokenType.ELSE_IF, "ELSE IF"),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP_LESS, "<"),
        Token(TokenType.NUMBER, "1"),
        Token(TokenType.THEN, "THEN"),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "B"),
        Token(TokenType.ELSE_IF, "ELSE IF"),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP_LESS, "<"),
        Token(TokenType.NUMBER, "1"),
        Token(TokenType.THEN, "THEN"),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "C"),
        Token(TokenType.ELSE, "ELSE"),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "D"),
        Token(TokenType.END_IF, "END_IF"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        IfStatementNode(
            Binary(VarNode("$x"), Token(TokenType.OP_GREATER, ">"), Literal("0")),
            [PrintStringNode(Literal("A"))],
            [
                IfStatementNode(
                    Binary(VarNode("$x"), Token(TokenType.OP_LESS, "<"), Literal("1")),
                    [PrintStringNode(Literal("B"))],
                ),
                IfStatementNode(
                    Binary(VarNode("$x"), Token(TokenType.OP_LESS, "<"), Literal("1")),
                    [PrintStringNode(Literal("C"))],
                ),
            ],
            [PrintStringNode(Literal("D"))],
        )
    ]
    assert ast == expected_ast


def test_print_string(parser):
    tokens = [
        Token(TokenType.PRINTSTRING, "PRINTSTRING"),
        Token(TokenType.STRING, "Hello, World!"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [PrintStringNode(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_while_statement(parser):
    tokens = [
        Token(TokenType.WHILE, "WHILE"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP_GREATER, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "Hello, World!"),
        Token(TokenType.END_WHILE, "END_WHILE"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStatementNode(
            Binary(VarNode("$x"), Token(TokenType.OP_GREATER, ">"), Literal("0")),
            [PrintStringNode(Literal("Hello, World!"))],
        )
    ]
    assert ast == expected_ast


def test_parentheses_priority_in_expression(parser):
    tokens = [
        Token(TokenType.VAR, "VAR"),
        Token(TokenType.ID, "$y"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.NUMBER, "3"),
        Token(TokenType.OP_MULTIPLY, "*"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP_PLUS, "+"),
        Token(TokenType.NUMBER, "2"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarDeclarationNode(
            "$y",
            Binary(
                Literal("3"),
                Token(TokenType.OP_MULTIPLY, "*"),
                Binary(VarNode("$x"), Token(TokenType.OP_PLUS, "+"), Literal("2")),
            ),
        )
    ]
    assert ast == expected_ast


def test_parentheses_in_simple_expression(parser):
    tokens = [
        Token(TokenType.VAR, "VAR"),
        Token(TokenType.ID, "$y"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.NUMBER, "1"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [VarDeclarationNode("$y", Literal("1"))]
    assert ast == expected_ast


def test_parentheses_in_while_statement(parser):
    tokens = [
        Token(TokenType.WHILE, "WHILE"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP_GREATER, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.END_WHILE, "END_WHILE"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStatementNode(
            Binary(VarNode("$x"), Token(TokenType.OP_GREATER, ">"), Literal("0")), []
        )
    ]
    assert ast == expected_ast


def test_while_statement_with_number(parser):
    tokens = [
        Token(TokenType.WHILE, "WHILE"),
        Token(TokenType.NUMBER, "10"),
        Token(TokenType.END_WHILE, "END_WHILE"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [WhileStatementNode(Literal("10"), [])]
    assert ast == expected_ast


def test_while_statement_without_parentheses(parser):
    tokens = [
        Token(TokenType.WHILE, "WHILE"),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP_GREATER, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.END_WHILE, "END_WHILE"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStatementNode(
            Binary(VarNode("$x"), Token(TokenType.OP_GREATER, ">"), Literal("0")), []
        )
    ]
    assert ast == expected_ast


def test_literals(parser):
    tokens = [
        Token(TokenType.FALSE, "FALSE"),
        Token(TokenType.TRUE, "TRUE"),
        Token(TokenType.NUMBER, "10"),
        Token(TokenType.STRING, "Hello, World!"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        Literal(False),
        Literal(True),
        Literal("10"),
        Literal("Hello, World!"),
    ]
    assert ast == expected_ast


def test_delay_statement(parser):
    tokens = [
        Token(TokenType.DELAY, "DELAY"),
        Token(TokenType.NUMBER, "10"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [DelayNode(Literal("10"))]
    assert ast == expected_ast


def test_unary_expression(parser):
    tokens = [
        Token(TokenType.OP_MINUS, "-"),
        Token(TokenType.NUMBER, "10"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [Unary(Token(TokenType.OP_MINUS, "-"), Literal("10"))]
    assert ast == expected_ast
