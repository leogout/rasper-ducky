import pytest
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def execute(code: str):
    lexer = Lexer()
    tokens = list(lexer.tokenize(code))
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)

    return interpreter


def test_if_statement():
    interpreter = execute(
        """
        VAR $x = 10
        VAR $y = 20
        IF $x < $y THEN
            STRING x is less than y
        END_IF
        """
    )

    # Vérification des résultats
    assert interpreter.variables["$x"] == 10
    assert interpreter.variables["$y"] == 20
    assert interpreter.execution_stack == ["x is less than y"]


def test_while_statement():
    interpreter = execute(
        """
        VAR $x = 5
        WHILE ($x > 0)
            STRING Hello, World!
            $x = $x - 1
        END_WHILE
        """
    )

    assert interpreter.variables["$x"] == 0
    assert interpreter.execution_stack == ["Hello, World!"] * 5


def test_assignment():
    interpreter = execute(
        """
        VAR $x = 10
        $x = $x + 1
        """
    )

    assert interpreter.variables["$x"] == 11


def test_priority():
    interpreter = execute(
        """
        VAR $x = 10
        $x = $x + 1 * 2
        """
    )

    assert interpreter.variables["$x"] == 12
