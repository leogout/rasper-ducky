import pytest
from parser import Parser, VarDeclarationNode, VarNode, NumberNode, ExpressionNode, OperatorNode, IfStatementNode, PrintStringNode, StringNode
from lexer import Token, TokenType

@pytest.fixture
def parser():
    def _parser(tokens):
        return Parser(tokens)
    return _parser

def test_var_declaration(parser):
    tokens = [
        Token(TokenType.VAR, 'VAR', 1, 0),
        Token(TokenType.ID, '$x', 1, 4),
        Token(TokenType.ASSIGN, '=', 1, 7),
        Token(TokenType.NUMBER, '10', 1, 9),
        Token(TokenType.EOF, '', 1, 12)
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarDeclarationNode("$x", NumberNode('10'))
    ]
    assert ast == expected_ast

def test_expression(parser):
    tokens = [
        Token(TokenType.VAR, 'VAR', 1, 0),
        Token(TokenType.ID, '$y', 1, 4),
        Token(TokenType.ASSIGN, '=', 1, 7),
        Token(TokenType.ID, '$x', 1, 9),
        Token(TokenType.OP, '*', 1, 12),
        Token(TokenType.NUMBER, '2', 1, 14),
        Token(TokenType.EOF, '', 1, 16)
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarDeclarationNode("$y", ExpressionNode(VarNode("$x"), OperatorNode('*'), NumberNode('2')))
    ]
    assert ast == expected_ast

def test_if_statement(parser):
    tokens = [
        Token(TokenType.IF, 'IF', 1, 0),
        Token(TokenType.ID, '$x', 1, 3),
        Token(TokenType.OP, '>', 1, 6),
        Token(TokenType.NUMBER, '0', 1, 8),
        Token(TokenType.THEN, 'THEN', 1, 10),
        Token(TokenType.VAR, 'VAR', 2, 0),
        Token(TokenType.ID, '$y', 2, 4),
        Token(TokenType.ASSIGN, '=', 2, 7),
        Token(TokenType.NUMBER, '1', 2, 9),
        Token(TokenType.END_IF, 'END_IF', 3, 0),
        Token(TokenType.EOF, '', 3, 7)
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        IfStatementNode(
            ExpressionNode(VarNode("$x"), OperatorNode('>'), NumberNode('0')),
            [VarDeclarationNode("$y", NumberNode('1'))]
        )
    ]
    assert ast == expected_ast
                                                                   
def test_print_string(parser):
    tokens = [
        Token(TokenType.PRINTSTRING, 'PRINTSTRING', 1, 0),
        Token(TokenType.STRING, 'Hello, World!', 1, 12),
        Token(TokenType.EOF, '', 1, 28)
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        PrintStringNode(StringNode('Hello, World!'))
    ]
    assert ast == expected_ast