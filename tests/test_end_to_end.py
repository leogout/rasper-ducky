import pytest
from rasper_ducky.interpreter.lexer import Lexer
from rasper_ducky.interpreter.parser import *
from rasper_ducky.interpreter.interpreter import Interpreter


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


def test_print_string():
    interpreter = execute("STRING Hello, World!")
    assert interpreter.execution_stack == ["Hello, World!"]


def test_print_stringln():
    interpreter = execute("STRINGLN Hello, World!")
    assert interpreter.execution_stack == ["Hello, World!"]


def test_booleans():
    interpreter = execute(
        """
        IF TRUE THEN 
            STRING A 
        END_IF
        IF FALSE THEN 
        ELSE 
            STRING B 
        END_IF
        """
    )
    assert interpreter.variables == {}
    assert interpreter.execution_stack == ["A", "B"]


def test_nested_if_statements():
    interpreter = execute(
        """
        IF TRUE THEN
            IF FALSE THEN
                STRING A
            ELSE
                IF TRUE THEN
                    STRING B
                ELSE
                    STRING C
                END_IF
            END_IF
        END_IF
        """
    )
    assert interpreter.execution_stack == ["B"]


def test_delay_statement(mocker):
    mock_sleep = mocker.patch("time.sleep")
    execute("DELAY 10")
    mock_sleep.assert_called_once_with(10)


def test_chained_assign_statement():
    interpreter = execute(
        """
        VAR $x = 10
        VAR $y = $x = 10
        """
    )
    assert interpreter.variables["$x"] == 10
    assert interpreter.variables["$y"] == 10


def test_function_declaration():
    interpreter = execute(
        """
        FUNCTION add()
            STRING Hello, World!
        END_FUNCTION
        add()
        add()
        add()
        add()
        """
    )

    assert interpreter.functions["add"] == [StringStmt(Literal("Hello, World!"))]
    assert interpreter.execution_stack == ["Hello, World!"] * 4


def test_global_variables():
    interpreter = execute(
        """
        FUNCTION add()
            $x = $x + 1
        END_FUNCTION

        VAR $x = 10
        add()
        add()
        add()
        """
    )
    assert interpreter.variables["$x"] == 13
