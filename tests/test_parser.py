import pytest
from parser import (
    Parser,
    VarDeclarationNode,
    VarNode,
    NumberNode,
    ExpressionNode,
    OperatorNode,
    IfStatementNode,
    PrintStringNode,
    StringNode,
    WhileStatementNode,
)
from lexer import Token, TokenType


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
    expected_ast = [VarDeclarationNode("$x", NumberNode("10"))]
    assert ast == expected_ast


def test_expression(parser):
    tokens = [
        Token(TokenType.VAR, "VAR"),
        Token(TokenType.ID, "$y"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP, "*"),
        Token(TokenType.NUMBER, "2"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarDeclarationNode(
            "$y", ExpressionNode(VarNode("$x"), OperatorNode("*"), NumberNode("2"))
        )
    ]
    assert ast == expected_ast


def test_if_else_statement(parser):
    tokens = [
        Token(TokenType.IF, "IF"),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP, ">"),
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
            ExpressionNode(VarNode("$x"), OperatorNode(">"), NumberNode("0")),
            [VarDeclarationNode("$y", NumberNode("1"))],
            [],
            [PrintStringNode(StringNode("Hey there!"))],
        )
    ]
    assert ast == expected_ast


def test_if_else_if_else_statement(parser):
    tokens = [
        Token(TokenType.IF, "IF"),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.THEN, "THEN"),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "A"),
        Token(TokenType.ELSE_IF, "ELSE IF"),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP, "<"),
        Token(TokenType.NUMBER, "1"),
        Token(TokenType.THEN, "THEN"),
        Token(TokenType.PRINTSTRING, "STRING"),
        Token(TokenType.STRING, "B"),
        Token(TokenType.ELSE_IF, "ELSE IF"),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP, "<"),
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
            ExpressionNode(VarNode("$x"), OperatorNode(">"), NumberNode("0")),
            [PrintStringNode(StringNode("A"))],
            [
                IfStatementNode(
                    ExpressionNode(VarNode("$x"), OperatorNode("<"), NumberNode("1")),
                    [PrintStringNode(StringNode("B"))],
                ),
                IfStatementNode(
                    ExpressionNode(VarNode("$x"), OperatorNode("<"), NumberNode("1")),
                    [PrintStringNode(StringNode("C"))],
                ),
            ],
            [PrintStringNode(StringNode("D"))],
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
    expected_ast = [PrintStringNode(StringNode("Hello, World!"))]
    assert ast == expected_ast


def test_while_statement(parser):
    tokens = [
        Token(TokenType.WHILE, "WHILE"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP, ">"),
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
            ExpressionNode(VarNode("$x"), OperatorNode(">"), NumberNode("0")),
            [PrintStringNode(StringNode("Hello, World!"))],
        )
    ]
    assert ast == expected_ast


def test_parentheses_priority_in_expression(parser):
    tokens = [
        Token(TokenType.VAR, "VAR"),
        Token(TokenType.ID, "$y"),
        Token(TokenType.ASSIGN, "="),
        Token(TokenType.NUMBER, "3"),
        Token(TokenType.OP, "*"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP, "+"),
        Token(TokenType.NUMBER, "2"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarDeclarationNode(
            "$y",
            ExpressionNode(
                NumberNode("3"),
                OperatorNode("*"),
                ExpressionNode(VarNode("$x"), OperatorNode("+"), NumberNode("2")),
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
    expected_ast = [VarDeclarationNode("$y", NumberNode("1"))]
    assert ast == expected_ast


def test_parentheses_in_while_statement(parser):
    tokens = [
        Token(TokenType.WHILE, "WHILE"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.END_WHILE, "END_WHILE"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStatementNode(
            ExpressionNode(VarNode("$x"), OperatorNode(">"), NumberNode("0")), []
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
    expected_ast = [WhileStatementNode(NumberNode("10"), [])]
    assert ast == expected_ast


def test_while_statement_without_parentheses(parser):
    tokens = [
        Token(TokenType.WHILE, "WHILE"),
        Token(TokenType.ID, "$x"),
        Token(TokenType.OP, ">"),
        Token(TokenType.NUMBER, "0"),
        Token(TokenType.END_WHILE, "END_WHILE"),
        Token(TokenType.EOF, ""),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStatementNode(
            ExpressionNode(VarNode("$x"), OperatorNode(">"), NumberNode("0")), []
        )
    ]
    assert ast == expected_ast
