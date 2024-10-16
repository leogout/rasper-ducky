from dataclasses import dataclass, field
from lexer import Tok, Token


# EXPRESSIONS
class Expr:
    pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __repr__(self):
        return f"EXPR({self.left}, {self.operator.value}, {self.right})"


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def __repr__(self):
        return f"EXPR({self.operator.value}, {self.right})"


@dataclass
class Literal(Expr):
    value: bool | int | str

    def __repr__(self):
        return f"LITERAL({self.value})"


@dataclass
class Grouping(Expr):
    expression: Expr

    def __repr__(self):
        return f"GROUP({self.expression})"


@dataclass
class Variable(Expr):
    name: Token

    def __repr__(self):
        return f"VAR({self.name})"


@dataclass
class Call(Expr):
    name: Token

    def __repr__(self):
        return f"CALL({self.callee})"


@dataclass
class Assign(Expr):
    name: Token
    value: Expr

    def __repr__(self):
        return f"ASSIGN({self.name}, {self.value})"


# STATEMENTS
class Stmt:
    pass


@dataclass
class VarStmt(Stmt):
    name: Token
    value: Expr

    def __repr__(self):
        return f"VAR_DECL({self.name}, {self.value})"


@dataclass
class DelayStmt(Stmt):
    value: Literal

    def __repr__(self):
        return f"DELAY({self.value})"


@dataclass
class StringStmt(Stmt):
    value: Literal

    def __repr__(self):
        return f"PRINT_STR({self.value})"


@dataclass
class StringLnStmt(Stmt):
    value: Literal

    def __repr__(self):
        return f"PRINT_STRLN({self.value})"


@dataclass
class IfStmt(Stmt):
    condition: Expr
    then_block: list[Stmt]
    else_if_blocks: list["IfStmt"] = field(default_factory=list)
    else_block: list[Stmt] = field(default_factory=list)

    def __repr__(self):
        return f"IF({self.condition}, {self.then_block}, {self.else_if_blocks}, {self.else_block})"


@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: list[Stmt]

    def __repr__(self):
        return f"WHILE({self.condition}, {self.body})"


@dataclass
class ExpressionStmt(Stmt):
    expression: Expr

    def __repr__(self):
        return f"EXPRESSION({self.expression})"


@dataclass
class FunctionStmt(Stmt):
    name: Token
    body: list[Stmt]

    def __repr__(self):
        return f"FUNCTION({self.name}, {self.body})"


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[Stmt]:
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def declaration(self) -> Stmt:
        if self.match(Tok.VAR):
            return self.var_stmt()
        return self.statement()

    def statement(self) -> Stmt:
        if self.match(Tok.VAR):
            return self.var_stmt()
        elif self.match(Tok.PRINTSTRING):
            return self.string_stmt()
        elif self.match(Tok.PRINTSTRINGLN):
            return self.stringln_stmt()
        elif self.match(Tok.DELAY):
            return self.delay_stmt()
        elif self.match(Tok.IF):
            return self.if_stmt()
        elif self.match(Tok.WHILE):
            return self.while_stmt()
        elif self.match(Tok.FUNCTION):
            return self.function_stmt()

        return self.expression_stmt()

    def var_stmt(self) -> VarStmt:
        name = self.consume(Tok.IDENTIFIER, "Expected an identifier after VAR")
        self.consume(Tok.ASSIGN, "Expected '=' after identifier")
        initializer = self.expression()
        self.consume(
            Tok.EOL,
            "Expected a line break after variable initialization",
        )
        return VarStmt(name, initializer)

    def string_stmt(self) -> StringStmt:
        value = self.consume(Tok.STRING, "Expected a string after STRING")
        self.consume(Tok.EOL, "Expected a line break after a string")
        return StringStmt(Literal(value.value))

    def stringln_stmt(self) -> StringLnStmt:
        value = self.consume(Tok.STRING, "Expected a string after STRINGLN")
        self.consume(Tok.EOL, "Expected a line break after a string")
        return StringLnStmt(Literal(value.value))

    def delay_stmt(self) -> DelayStmt:
        value = self.consume(Tok.NUMBER, "Expected a number after DELAY")
        self.consume(Tok.EOL, "Expected a line break after a number")
        return DelayStmt(Literal(value.value))

    def if_stmt(self) -> IfStmt:
        condition = self.expression()
        self.consume(Tok.THEN, "Expected 'THEN'")
        self.consume(Tok.EOL, "Expected a line break after 'THEN'")
        then_block = self.block()

        else_if_blocks = []
        while self.match(Tok.ELSE_IF):
            else_if_condition = self.expression()
            self.consume(Tok.THEN, "Expected 'THEN' after 'ELSE IF'")
            self.consume(Tok.EOL, "Expected a line break after 'THEN'")
            else_if_block = self.block()
            else_if_blocks.append(IfStmt(else_if_condition, else_if_block))

        else_block = []
        if self.match(Tok.ELSE):
            self.consume(Tok.EOL, "Expected a line break after 'ELSE'")
            else_block = self.block()
        self.consume(Tok.END_IF, "Expected 'END_IF'")
        self.consume(Tok.EOL, "Expected a line break after 'END_IF'")
        return IfStmt(condition, then_block, else_if_blocks, else_block)

    def while_stmt(self) -> WhileStmt:
        condition = self.expression()
        self.consume(Tok.EOL, "Expected a line break after the condition")
        body = self.block()
        self.consume(Tok.END_WHILE, "Expected 'END_WHILE'")
        self.consume(Tok.EOL, "Expected a line break after 'END_WHILE'")
        return WhileStmt(condition, body)

    def function_stmt(self) -> FunctionStmt:
        name = self.consume(Tok.IDENTIFIER, "Expected an identifier after FUNCTION")
        self.consume(Tok.LPAREN, "Expected '(' after function name")
        self.consume(Tok.RPAREN, "Expected ')' after function parameters")
        self.consume(Tok.EOL, "Expected a line break after the function parameters")
        body = self.block()
        self.consume(Tok.END_FUNCTION, "Expected 'END_FUNCTION'")
        self.consume(Tok.EOL, "Expected a line break after 'END_FUNCTION'")
        return FunctionStmt(name, body)

    def block(self) -> list[Stmt]:
        statements = []
        while (
            not self.check(Tok.END_IF)
            and not self.check(Tok.ELSE_IF)
            and not self.check(Tok.ELSE)
            and not self.check(Tok.END_WHILE)
            and not self.check(Tok.END_FUNCTION)
            and not self.is_at_end()
        ):
            statements.append(self.statement())
        return statements

    def expression_stmt(self) -> ExpressionStmt:
        expr = self.expression()
        self.consume(Tok.EOL, "Expected a line break after an expression")
        return ExpressionStmt(expr)

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.equality()

        if self.match(Tok.ASSIGN):
            value = self.assignment()  # allows for assignment chains like a = b = c = 1

            if isinstance(expr, Variable):
                return Assign(expr.name, value)

        return expr

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(Tok.OP_EQUAL, Tok.OP_NOT_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(
            Tok.OP_GREATER,
            Tok.OP_LESS,
            Tok.OP_GREATER_EQUAL,
            Tok.OP_LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(Tok.OP_PLUS, Tok.OP_MINUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(Tok.OP_MULTIPLY, Tok.OP_DIVIDE, Tok.OP_MODULO):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(Tok.OP_NOT, Tok.OP_MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.call()

    def call(self) -> Expr:
        expr = self.primary()
        name = self.previous()
        if self.match(Tok.LPAREN):
            self.consume(Tok.RPAREN, "Expected ')' after function call")
            return Call(name)

        return expr

    def primary(self) -> Expr:
        if self.match(Tok.FALSE):
            return Literal(False)
        if self.match(Tok.TRUE):
            return Literal(True)
        if self.match(Tok.NUMBER):
            return Literal(self.previous().value)
        if self.match(Tok.STRING):
            return Literal(self.previous().value)
        if self.match(Tok.IDENTIFIER):
            return Variable(self.previous())

        if self.match(Tok.LPAREN):
            expr = self.expression()
            self.consume(Tok.RPAREN, "Expected ')' after expression")
            return Grouping(expr)

        raise self.error(self.peek(), "Expected expression")

    def error(self, token: Token, message: str) -> SyntaxError:
        return SyntaxError(
            f"Unexpected token {token.type} at line {token.line}, column {token.column}: {message}"
        )

    def match(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.peek().type == Tok.EOF

    def consume(self, type, message) -> Token:
        if self.check(type):
            return self.advance()
        raise SyntaxError(message, self.peek().line, self.peek().column)

    def synchronize(self):
        # may be used later for error recovery
        self.advance()
        while not self.is_at_end():
            if self.previous().type == Tok.EOL:
                return
            if (
                self.peek().type == Tok.IF
                or self.peek().type == Tok.WHILE
                or self.peek().type == Tok.PRINTSTRING
                or self.peek().type == Tok.PRINTSTRINGLN
                or self.peek().type == Tok.DELAY
                or self.peek().type == Tok.FUNCTION
                or self.peek().type == Tok.RETURN
                or self.peek().type == Tok.KEYPRESS
            ):
                return
            self.advance()
