import pytest
from interpreter import *
from parser import *


@pytest.fixture
def interpreter():
    return Interpreter()


def test_var_declaration(interpreter):
    ast = [VarDeclarationNode("$x", Literal(10))]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 10


def test_expression_evaluation(interpreter):
    ast = [
        VarDeclarationNode("$x", Literal(10)),
        VarDeclarationNode(
            "$y", Binary(VarNode("$x"), Token(TokenType.OP_MULTIPLY, "*"), Literal(2))
        ),
        VarDeclarationNode(
            "$z", Binary(VarNode("$y"), Token(TokenType.OP_PLUS, "+"), Literal(5))
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$y"] == 20
    assert interpreter.variables["$z"] == 25


def test_print_string(interpreter):
    ast = [PrintStringNode(Literal("Hello, World!"))]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["Hello, World!"]


def test_variable_update(interpreter):
    ast = [
        VarDeclarationNode("$x", Literal(10)),
        VarDeclarationNode("$x", Literal(20)),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 20


def test_complex_expression(interpreter):
    ast = [
        VarDeclarationNode("$x", Literal(10)),
        VarDeclarationNode("$y", Literal(5)),
        VarDeclarationNode(
            "$z",
            Binary(
                Binary(VarNode("$x"), Token(TokenType.OP_PLUS, "+"), VarNode("$y")),
                Token(TokenType.OP_MULTIPLY, "*"),
                Literal(3),
            ),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$z"] == 45


def test_if_statement(interpreter):
    ast = [
        VarDeclarationNode("$x", Literal("1")),
        IfStatementNode(
            Binary(VarNode("$x"), Token(TokenType.OP_GREATER, ">"), Literal("0")),
            [PrintStringNode(Literal("A"))],
            [PrintStringNode(Literal("B"))],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["A"]


def test_else_statement(interpreter):
    ast = [
        VarDeclarationNode("$x", Literal("1")),
        IfStatementNode(
            Binary(VarNode("$x"), Token(TokenType.OP_LESS, "<"), Literal("0")),
            [PrintStringNode(Literal("A"))],
            [],
            [PrintStringNode(Literal("B"))],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["B"]


def test_one_else_if_statement(interpreter):
    ast = [
        VarDeclarationNode("$x", Literal("1")),
        IfStatementNode(
            Binary(VarNode("$x"), Token(TokenType.OP_LESS, "<"), Literal("0")),
            [PrintStringNode(Literal("A"))],
            [
                IfStatementNode(
                    Binary(
                        VarNode("$x"), Token(TokenType.OP_EQUAL, "=="), Literal("1")
                    ),
                    [PrintStringNode(Literal("B"))],
                ),
            ],
            [PrintStringNode(Literal("C"))],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["B"]


def test_multiple_else_if_statement(interpreter):
    ast = [
        VarDeclarationNode("$x", Literal("1")),
        IfStatementNode(
            Binary(VarNode("$x"), Token(TokenType.OP_LESS, "<"), Literal("0")),
            [PrintStringNode(Literal("A"))],
            [
                IfStatementNode(
                    Binary(
                        VarNode("$x"), Token(TokenType.OP_EQUAL, "=="), Literal("0")
                    ),
                    [PrintStringNode(Literal("B"))],
                ),
                IfStatementNode(
                    Binary(
                        VarNode("$x"), Token(TokenType.OP_EQUAL, "=="), Literal("1")
                    ),
                    [PrintStringNode(Literal("C"))],
                ),
            ],
            [PrintStringNode(Literal("D"))],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["C"]


def test_else_statement_with_else_if(interpreter):
    ast = [
        VarDeclarationNode("$x", Literal("1")),
        IfStatementNode(
            Binary(VarNode("$x"), Token(TokenType.OP_LESS, "<"), Literal("0")),
            [PrintStringNode(Literal("A"))],
            [
                IfStatementNode(
                    Binary(
                        VarNode("$x"), Token(TokenType.OP_EQUAL, "=="), Literal("0")
                    ),
                    [PrintStringNode(Literal("B"))],
                ),
            ],
            [PrintStringNode(Literal("D"))],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["D"]


def test_division_by_zero(interpreter):
    ast = [
        VarDeclarationNode("$x", Literal("10")),
        VarDeclarationNode(
            "$y", Binary(VarNode("$x"), Token(TokenType.OP_DIVIDE, "/"), Literal("0"))
        ),
    ]
    with pytest.raises(ZeroDivisionError):
        interpreter.interpret(ast)


def test_unknown_operator(interpreter):
    ast = [Binary(Literal("1"), Token(20000, "unknown"), Literal("2"))]
    with pytest.raises(RuntimeError, match="Opérateur inconnu"):
        interpreter.interpret(ast)


def test_undefined_variable(interpreter):
    ast = [Binary(VarNode("$undefined"), Token(TokenType.OP_PLUS, "+"), Literal("2"))]
    with pytest.raises(RuntimeError, match="Variable non définie"):
        interpreter.interpret(ast)


def test_logical_operators(interpreter):
    ast = [
        VarDeclarationNode(
            "$x", Binary(Literal("1"), Token(TokenType.OP_AND, "&&"), Literal("0"))
        ),
        VarDeclarationNode(
            "$y", Binary(Literal("1"), Token(TokenType.OP_OR, "||"), Literal("0"))
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 0
    assert interpreter.variables["$y"] == 1


def test_bitwise_operators(interpreter):
    ast = [
        VarDeclarationNode(
            "$x",
            Binary(Literal("1"), Token(TokenType.OP_BITWISE_AND, "&"), Literal("1")),
        ),
        VarDeclarationNode(
            "$y",
            Binary(Literal("1"), Token(TokenType.OP_BITWISE_OR, "|"), Literal("0")),
        ),
        VarDeclarationNode(
            "$z",
            Binary(Literal("1"), Token(TokenType.OP_SHIFT_LEFT, "<<"), Literal("2")),
        ),
        VarDeclarationNode(
            "$w",
            Binary(Literal("4"), Token(TokenType.OP_SHIFT_RIGHT, ">>"), Literal("1")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 1
    assert interpreter.variables["$y"] == 1
    assert interpreter.variables["$z"] == 4
    assert interpreter.variables["$w"] == 2


def test_empty_block(interpreter):
    ast = [
        IfStatementNode(
            Binary(Literal("1"), Token(TokenType.OP_EQUAL, "=="), Literal("1")), []
        )
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == []


def test_equality_and_inequality(interpreter):
    ast = [
        VarDeclarationNode(
            "$x", Binary(Literal("1"), Token(TokenType.OP_EQUAL, "=="), Literal("1"))
        ),
        VarDeclarationNode(
            "$y",
            Binary(Literal("1"), Token(TokenType.OP_NOT_EQUAL, "!="), Literal("2")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == True
    assert interpreter.variables["$y"] == True


def test_printstringln(interpreter):
    ast = [PrintStringLnNode(Literal("Hello, World!"))]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["Hello, World!"]


def test_while_statement(interpreter):
    ast = [
        VarDeclarationNode("$x", Literal("0")),
        WhileStatementNode(
            Binary(VarNode("$x"), Token(TokenType.OP_LESS, "<"), Literal("5")),
            [
                PrintStringNode(Literal("Hello, World!")),
                VarDeclarationNode(
                    "$x",
                    Binary(VarNode("$x"), Token(TokenType.OP_PLUS, "+"), Literal("1")),
                ),
            ],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 5
    assert interpreter.execution_stack == ["Hello, World!"] * 5


def test_literals(interpreter):
    ast = [Literal(False), Literal(True), Literal("10"), Literal("Hello, World!")]
    interpreter.interpret(ast)
    assert interpreter.variables == {}
    assert interpreter.execution_stack == []


def test_boolean_in_if_statement(interpreter):
    ast = [
        IfStatementNode(Literal(True), [PrintStringNode(Literal("A"))], []),
        IfStatementNode(Literal(False), [], [], [PrintStringNode(Literal("B"))]),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["A", "B"]


def test_delay_statement(interpreter, mocker):
    mock_sleep = mocker.patch("time.sleep")
    ast = [DelayNode(Literal("10"))]
    interpreter.interpret(ast)
    mock_sleep.assert_called_once_with(10)
    assert interpreter.execution_stack == []
