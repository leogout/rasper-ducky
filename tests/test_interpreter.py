import pytest
from interpreter import *
from parser import *


@pytest.fixture
def interpreter():
    return Interpreter()


def test_var_declaration(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal(10),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 10


def test_expression_evaluation(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal(10),
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "$y"),
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_MULTIPLY, "*"),
                Literal(2),
            ),
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "$z"),
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$y")),
                Token(TokenType.OP_PLUS, "+"),
                Literal(5),
            ),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$y"] == 20
    assert interpreter.variables["$z"] == 25


def test_print_string(interpreter):
    ast = [StringStmt(Literal("Hello, World!"))]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["Hello, World!"]


def test_variable_update(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal(10),
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal(20),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 20


def test_complex_expression(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal(10),
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "$y"),
            Literal(5),
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "$z"),
            Binary(
                Binary(
                    Variable(Token(TokenType.IDENTIFIER, "$x")),
                    Token(TokenType.OP_PLUS, "+"),
                    Variable(Token(TokenType.IDENTIFIER, "$y")),
                ),
                Token(TokenType.OP_MULTIPLY, "*"),
                Literal(3),
            ),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$z"] == 45


def test_if_statement(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal("1"),
        ),
        IfStmt(
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_GREATER, ">"),
                Literal("0"),
            ),
            [StringStmt(Literal("A"))],
            [StringStmt(Literal("B"))],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["A"]


def test_else_statement(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal("1"),
        ),
        IfStmt(
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_LESS, "<"),
                Literal("0"),
            ),
            [StringStmt(Literal("A"))],
            [],
            [StringStmt(Literal("B"))],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["B"]


def test_one_else_if_statement(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal("1"),
        ),
        IfStmt(
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_LESS, "<"),
                Literal("0"),
            ),
            [StringStmt(Literal("A"))],
            [
                IfStmt(
                    Binary(
                        Variable(Token(TokenType.IDENTIFIER, "$x")),
                        Token(TokenType.OP_EQUAL, "=="),
                        Literal("1"),
                    ),
                    [StringStmt(Literal("B"))],
                ),
            ],
            [StringStmt(Literal("C"))],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["B"]


def test_multiple_else_if_statement(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal("1"),
        ),
        IfStmt(
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_LESS, "<"),
                Literal("0"),
            ),
            [StringStmt(Literal("A"))],
            [
                IfStmt(
                    Binary(
                        Variable(Token(TokenType.IDENTIFIER, "$x")),
                        Token(TokenType.OP_EQUAL, "=="),
                        Literal("0"),
                    ),
                    [StringStmt(Literal("B"))],
                ),
                IfStmt(
                    Binary(
                        Variable(Token(TokenType.IDENTIFIER, "$x")),
                        Token(TokenType.OP_EQUAL, "=="),
                        Literal("1"),
                    ),
                    [StringStmt(Literal("C"))],
                ),
            ],
            [StringStmt(Literal("D"))],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["C"]


def test_else_statement_with_else_if(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal("1"),
        ),
        IfStmt(
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_LESS, "<"),
                Literal("0"),
            ),
            [StringStmt(Literal("A"))],
            [
                IfStmt(
                    Binary(
                        Variable(Token(TokenType.IDENTIFIER, "$x")),
                        Token(TokenType.OP_EQUAL, "=="),
                        Literal("0"),
                    ),
                    [StringStmt(Literal("B"))],
                ),
            ],
            [StringStmt(Literal("D"))],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["D"]


def test_division_by_zero(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal("10"),
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "$y"),
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_DIVIDE, "/"),
                Literal("0"),
            ),
        ),
    ]
    with pytest.raises(ZeroDivisionError):
        interpreter.interpret(ast)


def test_unknown_operator(interpreter):
    ast = [Binary(Literal("1"), Token(2000, "unknown"), Literal("2"))]
    with pytest.raises(RuntimeError, match="Opérateur inconnu"):
        interpreter.interpret(ast)


def test_undefined_variable(interpreter):
    ast = [
        Binary(
            Variable(Token(TokenType.IDENTIFIER, "$undefined")),
            Token(TokenType.OP_PLUS, "+"),
            Literal("2"),
        )
    ]
    with pytest.raises(RuntimeError, match="Variable non définie"):
        interpreter.interpret(ast)


def test_logical_operators(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Binary(Literal("1"), Token(TokenType.OP_AND, "&&"), Literal("0")),
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "$y"),
            Binary(Literal("1"), Token(TokenType.OP_OR, "||"), Literal("0")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 0
    assert interpreter.variables["$y"] == 1


def test_bitwise_operators(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Binary(Literal("1"), Token(TokenType.OP_BITWISE_AND, "&"), Literal("1")),
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "$y"),
            Binary(Literal("1"), Token(TokenType.OP_BITWISE_OR, "|"), Literal("0")),
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "$z"),
            Binary(Literal("1"), Token(TokenType.OP_SHIFT_LEFT, "<<"), Literal("2")),
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "$w"),
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
        IfStmt(Binary(Literal("1"), Token(TokenType.OP_EQUAL, "=="), Literal("1")), [])
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == []


def test_equality_and_inequality(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Binary(Literal("1"), Token(TokenType.OP_EQUAL, "=="), Literal("1")),
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "$y"),
            Binary(Literal("1"), Token(TokenType.OP_NOT_EQUAL, "!="), Literal("2")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == True
    assert interpreter.variables["$y"] == True


def test_printstringln(interpreter):
    ast = [StringLnStmt(Literal("Hello, World!"))]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["Hello, World!"]


def test_while_statement(interpreter):
    ast = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "$x"),
            Literal("0"),
        ),
        WhileStmt(
            Binary(
                Variable(Token(TokenType.IDENTIFIER, "$x")),
                Token(TokenType.OP_LESS, "<"),
                Literal("5"),
            ),
            [
                StringStmt(Literal("Hello, World!")),
                VarStmt(
                    Token(TokenType.IDENTIFIER, "$x"),
                    Binary(
                        Variable(Token(TokenType.IDENTIFIER, "$x")),
                        Token(TokenType.OP_PLUS, "+"),
                        Literal("1"),
                    ),
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
        IfStmt(Literal(True), [StringStmt(Literal("A"))], []),
        IfStmt(Literal(False), [], [], [StringStmt(Literal("B"))]),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["A", "B"]


def test_delay_statement(interpreter, mocker):
    mock_sleep = mocker.patch("time.sleep")
    ast = [DelayStmt(Literal("10"))]
    interpreter.interpret(ast)
    mock_sleep.assert_called_once_with(10)
    assert interpreter.execution_stack == []
