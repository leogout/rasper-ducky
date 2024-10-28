import pytest
from rasper_ducky.duckyscript.lexer import Lexer
from rasper_ducky.duckyscript.parser import *
from rasper_ducky.duckyscript.interpreter import Interpreter
from unittest.mock import call


@pytest.fixture
def mock_type_string(mocker):
    return mocker.patch("rasper_ducky.duckyscript.interpreter.type_string")


@pytest.fixture
def mock_press_key(mocker):
    return mocker.patch("rasper_ducky.duckyscript.interpreter.press_key")


@pytest.fixture
def mock_release_all(mocker):
    return mocker.patch("rasper_ducky.duckyscript.interpreter.release_all")


def execute(code: str):
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)

    return interpreter


def test_if_statement(mock_type_string):
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
    assert mock_type_string.call_count == 1
    mock_type_string.assert_called_with("x is less than y")


def test_while_statement(mock_type_string):
    interpreter = execute(
        """
        VAR $x = 5
        WHILE ($x > 0)
            STRING Hello, World!
            $x = $x - 1
        END_WHILE
        """
    )

    assert mock_type_string.call_count == 5
    mock_type_string.assert_called_with("Hello, World!")


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


def test_print_string(mock_type_string):
    interpreter = execute("STRING Hello, World!")
    assert mock_type_string.call_count == 1
    mock_type_string.assert_called_with("Hello, World!")


def test_print_stringln(mock_type_string):
    interpreter = execute("STRINGLN Hello, World!")
    assert mock_type_string.call_count == 1
    mock_type_string.assert_called_with("Hello, World!")


def test_booleans(mock_type_string):
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
    assert mock_type_string.call_count == 2
    mock_type_string.assert_has_calls([call("A"), call("B")])


def test_nested_if_statements(mock_type_string):
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
    assert mock_type_string.call_count == 1
    mock_type_string.assert_called_with("B")


def test_delay_statement(mocker):
    mock_sleep = mocker.patch("time.sleep")
    execute("DELAY 10")
    mock_sleep.assert_called_once_with(0.01)


def test_chained_assign_statement():
    interpreter = execute(
        """
        VAR $x = 10
        VAR $y = $x = 10
        """
    )
    assert interpreter.variables["$x"] == 10
    assert interpreter.variables["$y"] == 10


def test_function_declaration(mock_type_string):
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
    assert mock_type_string.call_count == 4
    mock_type_string.assert_has_calls([call("Hello, World!") for _ in range(4)])


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


def test_keypress_statement(mock_press_key, mock_release_all):
    execute("CTRL")
    mock_press_key.assert_has_calls([call("CTRL")])
    mock_release_all.assert_called_once()


def test_keypress_statement_with_multiple_keys(mock_press_key, mock_release_all):
    execute("CTRL ALT B")
    mock_press_key.assert_has_calls([call("CTRL"), call("ALT"), call("B")])
    mock_release_all.assert_called_once()
