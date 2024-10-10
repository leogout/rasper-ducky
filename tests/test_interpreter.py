import pytest
from interpreter import Interpreter
from parser import VarDeclarationNode, ExpressionNode, NumberNode, VarNode, PrintStringNode, StringNode, OperatorNode, IfStatementNode, WhileStatementNode


@pytest.fixture
def interpreter():
    return Interpreter()


def test_var_declaration(interpreter):
    ast = [
        VarDeclarationNode("$x", NumberNode(10))
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 10


def test_expression_evaluation(interpreter):
    ast = [
        VarDeclarationNode("$x", NumberNode(10)),
        VarDeclarationNode("$y", ExpressionNode(VarNode("$x"), OperatorNode('*'), NumberNode(2))),
        VarDeclarationNode("$z", ExpressionNode(VarNode("$y"), OperatorNode('+'), NumberNode(5)))
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$y"] == 20
    assert interpreter.variables["$z"] == 25

def test_print_string(interpreter):
    ast = [
        PrintStringNode(StringNode("Hello, World!"))
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["Hello, World!"]


def test_variable_update(interpreter):
    ast = [
        VarDeclarationNode("$x", NumberNode(10)),
        VarDeclarationNode("$x", NumberNode(20))
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 20


def test_complex_expression(interpreter):
    ast = [
        VarDeclarationNode("$x", NumberNode(10)),
        VarDeclarationNode("$y", NumberNode(5)),
        VarDeclarationNode("$z", ExpressionNode(
            ExpressionNode(VarNode("$x"), OperatorNode('+'), VarNode("$y")),
            OperatorNode('*'),
            NumberNode(3)
        ))
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$z"] == 45


def test_if_statement(interpreter):
    ast = [
        VarDeclarationNode("$x", NumberNode('1')),
        IfStatementNode(
            ExpressionNode(VarNode("$x"), OperatorNode('>'), NumberNode('0')),
            [PrintStringNode(StringNode('A'))],
            [PrintStringNode(StringNode('B'))]
        )
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ['A']


def test_else_statement(interpreter):
    ast = [
        VarDeclarationNode("$x", NumberNode('1')),
        IfStatementNode(
            ExpressionNode(VarNode("$x"), OperatorNode('<'), NumberNode('0')),
            [PrintStringNode(StringNode('A'))],
            [],
            [PrintStringNode(StringNode('B'))]
        )
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ['B']


def test_one_else_if_statement(interpreter):
    ast = [
        VarDeclarationNode("$x", NumberNode('1')),
        IfStatementNode(
            ExpressionNode(VarNode("$x"), OperatorNode('<'), NumberNode('0')),
            [PrintStringNode(StringNode('A'))],
            [
                IfStatementNode(
                    ExpressionNode(VarNode("$x"), OperatorNode('=='), NumberNode('1')),
                    [PrintStringNode(StringNode('B'))]
                ),
            ],
            [PrintStringNode(StringNode('C'))]
        )
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ['B']


def test_multiple_else_if_statement(interpreter):
    ast = [
        VarDeclarationNode("$x", NumberNode('1')),
        IfStatementNode(
            ExpressionNode(VarNode("$x"), OperatorNode('<'), NumberNode('0')),
            [PrintStringNode(StringNode('A'))],
            [
                IfStatementNode(
                    ExpressionNode(VarNode("$x"), OperatorNode('=='), NumberNode('0')),
                    [PrintStringNode(StringNode('B'))]
                ),
                IfStatementNode(
                    ExpressionNode(VarNode("$x"), OperatorNode('=='), NumberNode('1')),
                    [PrintStringNode(StringNode('C'))]
                ),
            ],
            [PrintStringNode(StringNode('D'))]
        )
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ['C']


def test_else_statement_with_else_if(interpreter):
    ast = [
        VarDeclarationNode("$x", NumberNode('1')),
        IfStatementNode(
            ExpressionNode(VarNode("$x"), OperatorNode('<'), NumberNode('0')),
            [PrintStringNode(StringNode('A'))],
            [
                IfStatementNode(
                    ExpressionNode(VarNode("$x"), OperatorNode('=='), NumberNode('0')),
                    [PrintStringNode(StringNode('B'))]
                ),
            ],
            [PrintStringNode(StringNode('D'))]
        )
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ['D']

def test_division_by_zero(interpreter):
    ast = [
        VarDeclarationNode("$x", NumberNode(10)),
        VarDeclarationNode("$y", ExpressionNode(VarNode("$x"), OperatorNode('/'), NumberNode(0)))
    ]
    with pytest.raises(ZeroDivisionError):
        interpreter.interpret(ast)

def test_unknown_operator(interpreter):
    ast = [
        ExpressionNode(NumberNode(1), OperatorNode('unknown'), NumberNode(2))
    ]
    with pytest.raises(RuntimeError, match="Opérateur inconnu"):
        interpreter.interpret(ast)

def test_undefined_variable(interpreter):
    ast = [
        ExpressionNode(VarNode("$undefined"), OperatorNode('+'), NumberNode(2))
    ]
    with pytest.raises(RuntimeError, match="Variable non définie"):
        interpreter.interpret(ast)

def test_logical_operators(interpreter):
    ast = [
        VarDeclarationNode("$x", ExpressionNode(NumberNode(1), OperatorNode('&&'), NumberNode(0))),
        VarDeclarationNode("$y", ExpressionNode(NumberNode(1), OperatorNode('||'), NumberNode(0)))
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 0
    assert interpreter.variables["$y"] == 1

def test_bitwise_operators(interpreter):
    ast = [
        VarDeclarationNode("$x", ExpressionNode(NumberNode(1), OperatorNode('&'), NumberNode(1))),
        VarDeclarationNode("$y", ExpressionNode(NumberNode(1), OperatorNode('|'), NumberNode(0))),
        VarDeclarationNode("$z", ExpressionNode(NumberNode(1), OperatorNode('<<'), NumberNode(2))),
        VarDeclarationNode("$w", ExpressionNode(NumberNode(4), OperatorNode('>>'), NumberNode(1)))
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 1
    assert interpreter.variables["$y"] == 1
    assert interpreter.variables["$z"] == 4
    assert interpreter.variables["$w"] == 2

def test_empty_block(interpreter):
    ast = [
        IfStatementNode(
            ExpressionNode(NumberNode(1), OperatorNode('=='), NumberNode(1)),
            []
        )
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == []

def test_equality_and_inequality(interpreter):
    ast = [
        VarDeclarationNode("$x", ExpressionNode(NumberNode(1), OperatorNode('=='), NumberNode(1))),
        VarDeclarationNode("$y", ExpressionNode(NumberNode(1), OperatorNode('!='), NumberNode(2)))
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == True
    assert interpreter.variables["$y"] == True

def test_while_statement(interpreter):
    ast = [
        VarDeclarationNode("$x", NumberNode(0)),
        WhileStatementNode(
            ExpressionNode(VarNode("$x"), OperatorNode('<'), NumberNode(5)),
            [
                VarDeclarationNode("$x", ExpressionNode(VarNode("$x"), OperatorNode('+'), NumberNode(1)))
            ]
        )
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 5

