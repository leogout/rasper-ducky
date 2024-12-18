import pytest
from rasper_ducky.duckyscript.parser import (
    KeyPressStmt,
    Parser,
    RandomCharFromStmt,
    Token,
    Tok,
    VarStmt,
    Binary,
    Variable,
    Literal,
    IfStmt,
    StringStmt,
    StringLnStmt,
    WhileStmt,
    Grouping,
    Call,
    FunctionStmt,
    KbdStmt,
    RandomCharStmt,
    DelayStmt,
    Unary,
    ExpressionStmt,
)


@pytest.fixture
def parser():
    def _parser(tokens):
        return Parser(tokens)

    return _parser


def test_var_declaration(parser):
    tokens = [
        Token(Tok.VAR, "VAR"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.ASSIGN, "="),
        Token(Tok.NUMBER, "10"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [VarStmt(Token(Tok.IDENTIFIER, "$x"), Literal("10"))]
    assert ast == expected_ast


def test_expression(parser):
    tokens = [
        Token(Tok.VAR, "VAR"),
        Token(Tok.IDENTIFIER, "$y"),
        Token(Tok.ASSIGN, "="),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_MULTIPLY, "*"),
        Token(Tok.NUMBER, "2"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_MULTIPLY, "*"),
                Literal("2"),
            ),
        )
    ]
    assert ast == expected_ast


def test_if_else_statement(parser):
    tokens = [
        Token(Tok.IF, "IF"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_GREATER, ">"),
        Token(Tok.NUMBER, "0"),
        Token(Tok.THEN, "THEN"),
        Token(Tok.EOL),
        Token(Tok.VAR, "VAR"),
        Token(Tok.IDENTIFIER, "$y"),
        Token(Tok.ASSIGN, "="),
        Token(Tok.NUMBER, "1"),
        Token(Tok.EOL),
        Token(Tok.ELSE, "ELSE"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "Hey there!"),
        Token(Tok.EOL),
        Token(Tok.END_IF, "END_IF"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        IfStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_GREATER, ">"),
                Literal("0"),
            ),
            [VarStmt(Token(Tok.IDENTIFIER, "$y"), Literal("1"))],
            [],
            [StringStmt(Literal("Hey there!"))],
        )
    ]
    assert ast == expected_ast


def test_string_statement(parser):
    tokens = [
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "Hello, World!"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [StringStmt(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_stringln_statement(parser):
    tokens = [
        Token(Tok.PRINTSTRINGLN, "STRINGLN"),
        Token(Tok.STRING, "Hello, World!"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [StringLnStmt(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_if_else_if_else_statement(parser):
    tokens = [
        Token(Tok.IF, "IF"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_GREATER, ">"),
        Token(Tok.NUMBER, "0"),
        Token(Tok.THEN, "THEN"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "A"),
        Token(Tok.EOL),
        Token(Tok.ELSE_IF, "ELSE IF"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_LESS, "<"),
        Token(Tok.NUMBER, "1"),
        Token(Tok.THEN, "THEN"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "B"),
        Token(Tok.EOL),
        Token(Tok.ELSE_IF, "ELSE IF"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_LESS, "<"),
        Token(Tok.NUMBER, "1"),
        Token(Tok.THEN, "THEN"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "C"),
        Token(Tok.EOL),
        Token(Tok.ELSE, "ELSE"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "D"),
        Token(Tok.EOL),
        Token(Tok.END_IF, "END_IF"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        IfStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_GREATER, ">"),
                Literal("0"),
            ),
            [StringStmt(Literal("A"))],
            [
                IfStmt(
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$x")),
                        Token(Tok.OP_LESS, "<"),
                        Literal("1"),
                    ),
                    [StringStmt(Literal("B"))],
                ),
                IfStmt(
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$x")),
                        Token(Tok.OP_LESS, "<"),
                        Literal("1"),
                    ),
                    [StringStmt(Literal("C"))],
                ),
            ],
            [StringStmt(Literal("D"))],
        )
    ]
    assert ast == expected_ast


def test_print_string(parser):
    tokens = [
        Token(Tok.PRINTSTRING, "PRINTSTRING"),
        Token(Tok.STRING, "Hello, World!"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [StringStmt(Literal("Hello, World!"))]
    assert ast == expected_ast


def test_while_statement(parser):
    tokens = [
        Token(Tok.WHILE, "WHILE"),
        Token(Tok.LPAREN, "("),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_GREATER, ">"),
        Token(Tok.NUMBER, "0"),
        Token(Tok.RPAREN, ")"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "Hello, World!"),
        Token(Tok.EOL),
        Token(Tok.END_WHILE, "END_WHILE"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStmt(
            Grouping(
                Binary(
                    Variable(Token(Tok.IDENTIFIER, "$x")),
                    Token(Tok.OP_GREATER, ">"),
                    Literal("0"),
                ),
            ),
            [StringStmt(Literal("Hello, World!"))],
        )
    ]
    assert ast == expected_ast


def test_parentheses_priority_in_expression(parser):
    tokens = [
        Token(Tok.VAR, "VAR"),
        Token(Tok.IDENTIFIER, "$y"),
        Token(Tok.ASSIGN, "="),
        Token(Tok.NUMBER, "3"),
        Token(Tok.OP_MULTIPLY, "*"),
        Token(Tok.LPAREN, "("),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_PLUS, "+"),
        Token(Tok.NUMBER, "2"),
        Token(Tok.RPAREN, ")"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        VarStmt(
            Token(Tok.IDENTIFIER, "$y"),
            Binary(
                Literal("3"),
                Token(Tok.OP_MULTIPLY, "*"),
                Grouping(
                    Binary(
                        Variable(Token(Tok.IDENTIFIER, "$x")),
                        Token(Tok.OP_PLUS, "+"),
                        Literal("2"),
                    ),
                ),
            ),
        )
    ]
    assert ast == expected_ast


def test_parentheses_in_simple_expression(parser):
    tokens = [
        Token(Tok.VAR, "VAR"),
        Token(Tok.IDENTIFIER, "$y"),
        Token(Tok.ASSIGN, "="),
        Token(Tok.LPAREN, "("),
        Token(Tok.NUMBER, "1"),
        Token(Tok.RPAREN, ")"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [VarStmt(Token(Tok.IDENTIFIER, "$y"), Grouping(Literal("1")))]
    assert ast == expected_ast


def test_parentheses_in_while_statement(parser):
    tokens = [
        Token(Tok.WHILE, "WHILE"),
        Token(Tok.LPAREN, "("),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_GREATER, ">"),
        Token(Tok.NUMBER, "0"),
        Token(Tok.RPAREN, ")"),
        Token(Tok.EOL),
        Token(Tok.END_WHILE, "END_WHILE"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStmt(
            Grouping(
                Binary(
                    Variable(Token(Tok.IDENTIFIER, "$x")),
                    Token(Tok.OP_GREATER, ">"),
                    Literal("0"),
                ),
            ),
            [],
        )
    ]
    assert ast == expected_ast


def test_while_statement_with_number(parser):
    tokens = [
        Token(Tok.WHILE, "WHILE"),
        Token(Tok.NUMBER, "10"),
        Token(Tok.EOL),
        Token(Tok.END_WHILE, "END_WHILE"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [WhileStmt(Literal("10"), [])]
    assert ast == expected_ast


def test_while_statement_without_parentheses(parser):
    tokens = [
        Token(Tok.WHILE, "WHILE"),
        Token(Tok.IDENTIFIER, "$x"),
        Token(Tok.OP_GREATER, ">"),
        Token(Tok.NUMBER, "0"),
        Token(Tok.EOL),
        Token(Tok.END_WHILE, "END_WHILE"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        WhileStmt(
            Binary(
                Variable(Token(Tok.IDENTIFIER, "$x")),
                Token(Tok.OP_GREATER, ">"),
                Literal("0"),
            ),
            [],
        )
    ]
    assert ast == expected_ast


def test_literals(parser):
    tokens = [
        Token(Tok.FALSE, "FALSE"),
        Token(Tok.EOL),
        Token(Tok.TRUE, "TRUE"),
        Token(Tok.EOL),
        Token(Tok.NUMBER, "10"),
        Token(Tok.EOL),
        Token(Tok.STRING, "Hello, World!"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        ExpressionStmt(Literal(False)),
        ExpressionStmt(Literal(True)),
        ExpressionStmt(Literal("10")),
        ExpressionStmt(Literal("Hello, World!")),
    ]
    assert ast == expected_ast


def test_delay_statement(parser):
    tokens = [
        Token(Tok.DELAY, "DELAY"),
        Token(Tok.NUMBER, "10"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [DelayStmt(Literal("10"))]
    assert ast == expected_ast


def test_unary_expression(parser):
    tokens = [
        Token(Tok.OP_MINUS, "-"),
        Token(Tok.NUMBER, "10"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [ExpressionStmt(Unary(Token(Tok.OP_MINUS, "-"), Literal("10")))]
    assert ast == expected_ast


def test_function_declaration(parser):
    tokens = [
        Token(Tok.FUNCTION, "FUNCTION"),
        Token(Tok.IDENTIFIER, "myFunction"),
        Token(Tok.LPAREN, "("),
        Token(Tok.RPAREN, ")"),
        Token(Tok.EOL),
        Token(Tok.PRINTSTRING, "STRING"),
        Token(Tok.STRING, "Hello, World!"),
        Token(Tok.EOL),
        Token(Tok.END_FUNCTION, "END_FUNCTION"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        FunctionStmt(
            Token(Tok.IDENTIFIER, "myFunction"),
            [StringStmt(Literal("Hello, World!"))],
        )
    ]
    assert ast == expected_ast


def test_function_call(parser):
    tokens = [
        Token(Tok.IDENTIFIER, "myFunction"),
        Token(Tok.LPAREN, "("),
        Token(Tok.RPAREN, ")"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [ExpressionStmt(Call(Token(Tok.IDENTIFIER, "myFunction")))]
    assert ast == expected_ast


def test_kbd_statement(parser):
    tokens = [
        Token(Tok.RD_KBD, "RD_KBD"),
        Token(Tok.RD_KBD_PLATFORM, "WIN"),
        Token(Tok.RD_KBD_LANGUAGE, "FR"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        KbdStmt(Token(Tok.RD_KBD_PLATFORM, "WIN"), Token(Tok.RD_KBD_LANGUAGE, "FR"))
    ]
    assert ast == expected_ast


def test_random_commands(parser):
    tokens = [
        Token(Tok.RANDOM_CHAR, "RANDOM_LOWERCASE_LETTER"),
        Token(Tok.EOL),
        Token(Tok.RANDOM_CHAR, "RANDOM_UPPERCASE_LETTER"),
        Token(Tok.EOL),
        Token(Tok.RANDOM_CHAR, "RANDOM_LETTER"),
        Token(Tok.EOL),
        Token(Tok.RANDOM_CHAR, "RANDOM_NUMBER"),
        Token(Tok.EOL),
        Token(Tok.RANDOM_CHAR, "RANDOM_SPECIAL"),
        Token(Tok.EOL),
        Token(Tok.RANDOM_CHAR, "RANDOM_CHAR"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_LOWERCASE_LETTER")),
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_UPPERCASE_LETTER")),
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_LETTER")),
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_NUMBER")),
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_SPECIAL")),
        RandomCharStmt(Token(Tok.RANDOM_CHAR, "RANDOM_CHAR")),
    ]
    assert ast == expected_ast


def test_random_char_from_statement(parser):
    tokens = [
        Token(Tok.RANDOM_CHAR_FROM, "RANDOM_CHAR_FROM"),
        Token(Tok.STRING, "aAzZ!#1,;:!()"),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        RandomCharFromStmt(
            Token(Tok.RANDOM_CHAR_FROM, "RANDOM_CHAR_FROM"),
            Literal("aAzZ!#1,;:!()"),
        )
    ]
    assert ast == expected_ast

def test_keypress_hold_release_statement(parser):
    tokens = [
        Token(Tok.KEYPRESS, "A"),
        Token(Tok.EOL),
        Token(Tok.HOLD, "HOLD"),
        Token(Tok.KEYPRESS, "A"),
        Token(Tok.EOL),
        Token(Tok.RELEASE, "RELEASE"),
        Token(Tok.KEYPRESS, "A"),
        Token(Tok.EOL),
        Token(Tok.EOF),
    ]
    ast = parser(tokens).parse()
    expected_ast = [
        KeyPressStmt([Token(Tok.KEYPRESS, "A")], False, False),
        KeyPressStmt([Token(Tok.KEYPRESS, "A")], True, False),
        KeyPressStmt([Token(Tok.KEYPRESS, "A")], False, True),
    ]
    assert ast == expected_ast
