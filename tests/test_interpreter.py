import pytest
from rasper_ducky.duckyscript.interpreter import (
    Interpreter,
)
from rasper_ducky.duckyscript.parser import (
    RandomCharFromStmt,
    Token,
    Tok,
    VarStmt,
    Literal,
    Binary,
    Unary,
    Variable,
    IfStmt,
    StringStmt,
    StringLnStmt,
    WhileStmt,
    DelayStmt,
    KbdStmt,
    RandomCharStmt,
    KeyPressStmt,
    Grouping,
    Assign,
    Call,
    FunctionStmt,
    ExpressionStmt,
)


@pytest.fixture
def interpreter():
    return Interpreter()


@pytest.fixture
def mock_keyboard(mocker):
    mock_press = mocker.patch("rasper_ducky.duckyscript.keyboard.RasperDuckyKeyboard.press_key")
    mock_release = mocker.patch("rasper_ducky.duckyscript.keyboard.RasperDuckyKeyboard.release_key")
    mock_release_all = mocker.patch("rasper_ducky.duckyscript.keyboard.RasperDuckyKeyboard.release_all")
    return mock_press, mock_release, mock_release_all


def test_var_declaration(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Literal(10),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 10


def test_expression_evaluation(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Literal(10),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_MULTIPLY, "*"),
                Literal(2),
            ),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$z"),
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$y")),
                Token(Tok.OP_PLUS, "+"),
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
            Token(Tok.IDENTIFIER, "$x"),
            Literal(10),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Literal(20),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 20


def test_complex_expression(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Literal(10),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Literal(5),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$z"),
            Binary(
                Binary(
                    Variable(Token(Tok.IDENTIFIER, "$x")),
                    Token(Tok.OP_PLUS, "+"),
                    Variable(Token(Tok.IDENTIFIER, "$y")),
                ),
                Token(Tok.OP_MULTIPLY, "*"),
                Literal(3),
            ),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$z"] == 45


def test_if_statement(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Literal("1"),
        ),
        IfStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_GREATER, ">"),
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
            Token(Tok.IDENTIFIER, "$x"),
            Literal("1"),
        ),
        IfStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_LESS, "<"),
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
            Token(Tok.IDENTIFIER, "$x"),
            Literal("1"),
        ),
        IfStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_LESS, "<"),
                Literal("0"),
            ),
            [StringStmt(Literal("A"))],
            [
                IfStmt(
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$x")),
                        Token(Tok.OP_EQUAL, "=="),
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
            Token(Tok.IDENTIFIER, "$x"),
            Literal("1"),
        ),
        IfStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_LESS, "<"),
                Literal("0"),
            ),
            [StringStmt(Literal("A"))],
            [
                IfStmt(
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$x")),
                        Token(Tok.OP_EQUAL, "=="),
                        Literal("0"),
                    ),
                    [StringStmt(Literal("B"))],
                ),
                IfStmt(
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$x")),
                        Token(Tok.OP_EQUAL, "=="),
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
            Token(Tok.IDENTIFIER, "$x"),
            Literal("1"),
        ),
        IfStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_LESS, "<"),
                Literal("0"),
            ),
            [StringStmt(Literal("A"))],
            [
                IfStmt(
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$x")),
                        Token(Tok.OP_EQUAL, "=="),
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
            Token(Tok.IDENTIFIER, "$x"),
            Literal("10"),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_DIVIDE, "/"),
                Literal("0"),
            ),
        ),
    ]
    with pytest.raises(ZeroDivisionError):
        interpreter.interpret(ast)


def test_unknown_operator(interpreter):
    ast = [Binary(Literal("1"), Token(2000, "unknown"), Literal("2"))]
    with pytest.raises(RuntimeError, match="Unknown operator: unknown"):
        interpreter.interpret(ast)


def test_undefined_variable(interpreter):
    ast = [
        Binary(
            Variable(Token(Tok.IDENTIFIER, "$undefined")),
            Token(Tok.OP_PLUS, "+"),
            Literal("2"),
        )
    ]
    with pytest.raises(RuntimeError, match=r"Undefined variable: \$undefined"):
        interpreter.interpret(ast)


def test_logical_operators(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Binary(Literal("1"), Token(Tok.OP_AND, "&&"), Literal("0")),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Binary(Literal("1"), Token(Tok.OP_OR, "||"), Literal("0")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 0
    assert interpreter.variables["$y"] == 1


def test_bitwise_operators(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Binary(Literal("1"), Token(Tok.OP_BITWISE_AND, "&"), Literal("1")),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Binary(Literal("1"), Token(Tok.OP_BITWISE_OR, "|"), Literal("0")),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$z"),
            Binary(Literal("1"), Token(Tok.OP_SHIFT_LEFT, "<<"), Literal("2")),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$w"),
            Binary(Literal("4"), Token(Tok.OP_SHIFT_RIGHT, ">>"), Literal("1")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 1
    assert interpreter.variables["$y"] == 1
    assert interpreter.variables["$z"] == 4
    assert interpreter.variables["$w"] == 2


def test_empty_block(interpreter):
    ast = [IfStmt(Binary(Literal("1"), Token(Tok.OP_EQUAL, "=="), Literal("1")), [])]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == []


def test_equality_and_inequality(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Binary(Literal("1"), Token(Tok.OP_EQUAL, "=="), Literal("1")),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Binary(Literal("1"), Token(Tok.OP_NOT_EQUAL, "!="), Literal("2")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"]
    assert interpreter.variables["$y"]


def test_printstringln(interpreter):
    ast = [StringLnStmt(Literal("Hello, World!"))]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["Hello, World!"]


def test_while_statement(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Literal("0"),
        ),
        WhileStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_LESS, "<"),
                Literal("5"),
            ),
            [
                StringStmt(Literal("Hello, World!")),
                VarStmt(
                    Token(Tok.IDENTIFIER, "$x"),
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$x")),
                        Token(Tok.OP_PLUS, "+"),
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
    mock_sleep.assert_called_once_with(0.01)
    assert interpreter.execution_stack == []


def test_kbd_statement(interpreter):
    ast = [KbdStmt(Token(Tok.RD_KBD_PLATFORM, "WIN"), Token(Tok.RD_KBD_LANGUAGE, "FR"))]
    interpreter.interpret(ast)
    assert interpreter.keyboard.platform == "win"
    assert interpreter.keyboard.language == "fr"


def test_random_char_statement(interpreter, mocker):
    mock_choice = mocker.patch("random.choice")

    ast = [
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_LOWERCASE_LETTER")),
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_UPPERCASE_LETTER")),
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_LETTER")),
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_NUMBER")),
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_SPECIAL")),
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_CHAR")),
    ]
    interpreter.interpret(ast)
    assert mock_choice.call_count == len(Interpreter.RANDOM_CHAR_SETS)

    for value in Interpreter.RANDOM_CHAR_SETS.values():
        mock_choice.assert_any_call(value)


def test_random_char_from_statement(interpreter, mocker):
    mock_choice = mocker.patch("random.choice")

    ast = [
        RandomCharFromStmt(
            Token(Tok.RANDOM_CHAR_FROM, "RANDOM_CHAR_FROM"),
            Literal("aAzZ!#1,;:!()"),
        ),
    ]
    interpreter.interpret(ast)
    assert mock_choice.call_count == 1
    mock_choice.assert_any_call("aAzZ!#1,;:!()")


def test_keypress_statement(interpreter, mock_keyboard):
    mock_press, mock_release, mock_release_all = mock_keyboard

    ast = [KeyPressStmt([Token(Tok.KEYPRESS, "A")])]
    interpreter.interpret(ast)

    mock_press.assert_called_once_with("A")
    mock_release.assert_not_called()
    mock_release_all.assert_called_once()


def test_keypress_statement_with_hold(interpreter, mock_keyboard):
    mock_press, mock_release, mock_release_all = mock_keyboard

    ast = [KeyPressStmt([Token(Tok.KEYPRESS, "A")], hold=True)]
    interpreter.interpret(ast)

    mock_press.assert_called_once_with("A")
    mock_release.assert_not_called()
    mock_release_all.assert_not_called()


def test_keypress_statement_with_release(interpreter, mock_keyboard):
    mock_press, mock_release, mock_release_all = mock_keyboard

    ast = [KeyPressStmt([Token(Tok.KEYPRESS, "A")], release=True)]
    interpreter.interpret(ast)

    mock_press.assert_not_called()
    mock_release.assert_called_once_with("A")
    mock_release_all.assert_not_called()


def test_unary_plus_operator(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Unary(Token(Tok.OP_PLUS, "+"), Literal("42")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 42


def test_unary_minus_operator(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Unary(Token(Tok.OP_MINUS, "-"), Literal("42")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == -42


def test_unary_not_operator(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Unary(Token(Tok.OP_NOT, "!"), Literal(True)),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Unary(Token(Tok.OP_NOT, "!"), Literal(False)),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] is False
    assert interpreter.variables["$y"] is True


def test_double_unary_minus(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Unary(
                Token(Tok.OP_MINUS, "-"),
                Unary(Token(Tok.OP_MINUS, "-"), Literal("42")),
            ),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 42


def test_unary_with_variable(interpreter):
    ast = [
        VarStmt(Token(Tok.IDENTIFIER, "$x"), Literal("10")),
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Unary(Token(Tok.OP_MINUS, "-"), Variable(Token(Tok.IDENTIFIER, "$x"))),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$y"] == -10


def test_grouping_basic(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Grouping(Literal("42")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 42


def test_grouping_precedence(interpreter):
    # (2 + 3) * 4 should be 20, not 14
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Binary(
                Grouping(
                    Binary(
                        Literal("2"),
                        Token(Tok.OP_PLUS, "+"),
                        Literal("3"),
                    )
                ),
                Token(Tok.OP_MULTIPLY, "*"),
                Literal("4"),
            ),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 20


def test_nested_grouping(interpreter):
    # ((2 + 3) * 4) + 1 should be 21
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Binary(
                Grouping(
                    Binary(
                        Grouping(
                            Binary(
                                Literal("2"),
                                Token(Tok.OP_PLUS, "+"),
                                Literal("3"),
                            )
                        ),
                        Token(Tok.OP_MULTIPLY, "*"),
                        Literal("4"),
                    )
                ),
                Token(Tok.OP_PLUS, "+"),
                Literal("1"),
            ),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 21


# 3. Assign expression tests
def test_inline_assignment(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Assign(Token(Tok.IDENTIFIER, "$x"), Literal("5")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 5
    assert interpreter.variables["$y"] == 5


# 4. Comparison operator tests
def test_less_than_or_equal(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Binary(Literal("5"), Token(Tok.OP_LESS_EQUAL, "<="), Literal("5")),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Binary(Literal("4"), Token(Tok.OP_LESS_EQUAL, "<="), Literal("5")),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$z"),
            Binary(Literal("6"), Token(Tok.OP_LESS_EQUAL, "<="), Literal("5")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] is True
    assert interpreter.variables["$y"] is True
    assert interpreter.variables["$z"] is False


def test_greater_than_or_equal(interpreter):
    ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$x"),
            Binary(Literal("5"), Token(Tok.OP_GREATER_EQUAL, ">="), Literal("5")),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Binary(Literal("6"), Token(Tok.OP_GREATER_EQUAL, ">="), Literal("5")),
        ),
        VarStmt(
            Token(Tok.IDENTIFIER, "$z"),
            Binary(Literal("4"), Token(Tok.OP_GREATER_EQUAL, ">="), Literal("5")),
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] is True
    assert interpreter.variables["$y"] is True
    assert interpreter.variables["$z"] is False


# 5. Function call tests
def test_function_call_basic(interpreter):
    ast = [
        FunctionStmt(
            Token(Tok.IDENTIFIER, "test_func"),
            [StringStmt(Literal("Hello from function"))],
        ),
        ExpressionStmt(Call(Token(Tok.IDENTIFIER, "test_func"))),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["Hello from function"]


def test_function_call_with_variable_modification(interpreter):
    ast = [
        VarStmt(Token(Tok.IDENTIFIER, "$x"), Literal("0")),
        FunctionStmt(
            Token(Tok.IDENTIFIER, "increment"),
            [
                VarStmt(
                    Token(Tok.IDENTIFIER, "$x"),
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$x")),
                        Token(Tok.OP_PLUS, "+"),
                        Literal("1"),
                    ),
                )
            ],
        ),
        ExpressionStmt(Call(Token(Tok.IDENTIFIER, "increment"))),
        ExpressionStmt(Call(Token(Tok.IDENTIFIER, "increment"))),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 2


# 8. Error handling edge cases
def test_unknown_random_char_set(interpreter):
    ast = [RandomCharStmt(Token(Tok.RANDOM_CHAR, "UNKNOWN_SET"))]
    with pytest.raises(RuntimeError, match="Unknown random character set"):
        interpreter.interpret(ast)


# 9. Stress tests for stack-based interpreter
def test_deeply_nested_expressions(interpreter):
    # Create expression: ((((1 + 1) + 1) + 1) + ... ) 100 times
    expr = Literal("1")
    for _ in range(100):
        expr = Binary(expr, Token(Tok.OP_PLUS, "+"), Literal("1"))
    
    ast = [VarStmt(Token(Tok.IDENTIFIER, "$x"), expr)]
    interpreter.interpret(ast)
    assert interpreter.variables["$x"] == 101


def test_long_while_loop(interpreter):
    # While loop that runs 1000 times
    ast = [
        VarStmt(Token(Tok.IDENTIFIER, "$counter"), Literal("0")),
        WhileStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$counter")),
                Token(Tok.OP_LESS, "<"),
                Literal("1000"),
            ),
            [
                VarStmt(
                    Token(Tok.IDENTIFIER, "$counter"),
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$counter")),
                        Token(Tok.OP_PLUS, "+"),
                        Literal("1"),
                    ),
                ),
            ],
        ),
    ]
    interpreter.interpret(ast)
    assert interpreter.variables["$counter"] == 1000


def test_deeply_nested_if_statements(interpreter):
    # Create 50 nested if statements
    innermost = [StringStmt(Literal("deep"))]
    stmt = IfStmt(Literal(True), innermost)
    
    for _ in range(49):
        stmt = IfStmt(Literal(True), [stmt])
    
    ast = [stmt]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == ["deep"]


# 10. Empty/edge case tests
def test_empty_ast(interpreter):
    ast = []
    interpreter.interpret(ast)
    assert interpreter.variables == {}
    assert interpreter.execution_stack == []


def test_empty_function_body(interpreter):
    ast = [
        FunctionStmt(Token(Tok.IDENTIFIER, "empty_func"), []),
        ExpressionStmt(Call(Token(Tok.IDENTIFIER, "empty_func"))),
    ]
    interpreter.interpret(ast)
    assert interpreter.execution_stack == []
