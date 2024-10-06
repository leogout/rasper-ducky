import pytest
from interpreter import Interpreter
from parser import VarDeclarationNode, ExpressionNode, NumberNode, VarNode, PrintStringNode, StringNode, OperatorNode


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