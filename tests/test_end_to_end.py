import pytest
from rasper_ducky.duckyscript.lexer import Lexer
from rasper_ducky.duckyscript.parser import Literal, Parser, StringStmt
from rasper_ducky.duckyscript.interpreter import Interpreter
from rasper_ducky.duckyscript.preprocessor import Preprocessor
from unittest.mock import call


@pytest.fixture
def mock_keyboard(mocker):
    mock_type_string = mocker.patch("rasper_ducky.duckyscript.interpreter.RasperDuckyKeyboard.type_string")
    mock_press = mocker.patch("rasper_ducky.duckyscript.keyboard.RasperDuckyKeyboard.press_key")
    mock_release = mocker.patch("rasper_ducky.duckyscript.keyboard.RasperDuckyKeyboard.release_key")
    mock_release_all = mocker.patch("rasper_ducky.duckyscript.keyboard.RasperDuckyKeyboard.release_all")
    return mock_type_string, mock_press, mock_release, mock_release_all


def execute(code: str):
    preprocessor = Preprocessor()
    code = preprocessor.process(code)
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)

    return interpreter


def test_if_statement(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

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


def test_while_statement(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

    execute(
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


def test_print_string(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

    execute("STRING Hello, World!")
    assert mock_type_string.call_count == 1
    mock_type_string.assert_called_with("Hello, World!")


def test_print_stringln(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

    execute("STRINGLN Hello, World!")
    assert mock_type_string.call_count == 1
    mock_type_string.assert_called_with("Hello, World!")


def test_booleans(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

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


def test_nested_if_statements(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

    execute(
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


def test_function_declaration(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

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


def test_keypress_statement(mock_keyboard):
    _, mock_press, _, mock_release_all = mock_keyboard

    execute("CTRL")
    mock_press.assert_has_calls([call("CTRL")])
    mock_release_all.assert_called_once()


def test_keypress_statement_with_multiple_keys(mock_keyboard):
    _, mock_press, _, mock_release_all = mock_keyboard

    execute("CTRL ALT B")
    mock_press.assert_has_calls([call("CTRL"), call("ALT"), call("B")])
    mock_release_all.assert_called_once()


def test_logical_operator_and(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

    execute(
        """
        IF (TRUE && TRUE) THEN
            STRING A
        END_IF
        IF (TRUE && FALSE) THEN
            STRING B
        END_IF
        IF (FALSE && FALSE) THEN
            STRING C
        END_IF
    """
    )
    assert mock_type_string.call_count == 1
    mock_type_string.assert_called_with("A")


def test_logical_operator_or(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

    execute(
        """
        IF (TRUE || TRUE) THEN
            STRING A
        END_IF
        IF (TRUE || FALSE) THEN
            STRING B
        END_IF
        IF (FALSE || FALSE) THEN
            STRING C
        END_IF
    """
    )
    assert mock_type_string.call_count == 2
    mock_type_string.assert_has_calls([call("A"), call("B")])


def test_unary_operator_not(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

    execute(
        """
        IF (!FALSE) THEN
            STRING A
        END_IF
        IF (!TRUE) THEN
            STRING B
        END_IF
    """
    )
    assert mock_type_string.call_count == 1
    mock_type_string.assert_called_with("A")


def test_unary_operator_minus():
    interpreter = execute("VAR $x = -10")
    assert interpreter.variables["$x"] == -10


def test_multiple_conditions(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

    execute(
        """
        IF ((TRUE == TRUE) && (FALSE == FALSE)) THEN
            STRING True
        END_IF
        """
    )
    assert mock_type_string.call_count == 1
    mock_type_string.assert_called_with("True")


def test_define_statement(mock_keyboard):
    mock_type_string, _, _, _ = mock_keyboard

    execute(
        """
        DEFINE #COUNT 3
        IF #COUNT == 3 THEN
            STRING A
        END_IF
    """
    )
    assert mock_type_string.call_count == 1
    mock_type_string.assert_called_with("A")


def test_random_char_statement(mocker):
    mock_choice = mocker.patch("random.choice")

    execute(
        """
        RANDOM_LOWERCASE_LETTER
        RANDOM_UPPERCASE_LETTER
        RANDOM_LETTER
        RANDOM_NUMBER
        RANDOM_SPECIAL
        RANDOM_CHAR
    """
    )

    assert mock_choice.call_count == len(Interpreter.RANDOM_CHAR_SETS)

    for value in Interpreter.RANDOM_CHAR_SETS.values():
        mock_choice.assert_any_call(value)


def test_random_char_from_statement(mocker):
    mock_choice = mocker.patch("random.choice")

    execute("RANDOM_CHAR_FROM aAzZ!#1,;:!()")

    assert mock_choice.call_count == 1
    mock_choice.assert_any_call("aAzZ!#1,;:!()")


def test_release_statement(mock_keyboard):
    _, _, mock_release, _ = mock_keyboard

    execute("RELEASE CTRL")
    mock_release.assert_called_once_with("CTRL")


def test_hold_statement(mock_keyboard):
    _, mock_press, _, mock_release_all = mock_keyboard

    execute("HOLD CTRL")
    mock_press.assert_called_once_with("CTRL")
    mock_release_all.assert_not_called()

