from dataclasses import dataclass, field
from lexer import TokenType, Token


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
        # try:
        if self.match(TokenType.VAR):
            return self.var_stmt()
        return self.statement()
        # except SyntaxError as e:
        #     self.synchronize()
        #     return None

    def statement(self) -> Stmt:
        if self.match(TokenType.VAR):
            return self.var_stmt()
        elif self.match(TokenType.PRINTSTRING):
            return self.string_stmt()
        elif self.match(TokenType.PRINTSTRINGLN):
            return self.stringln_stmt()
        elif self.match(TokenType.DELAY):
            return self.delay_stmt()
        elif self.match(TokenType.IF):
            return self.if_stmt()
        elif self.match(TokenType.WHILE):
            return self.while_stmt()
        elif self.match(TokenType.IDENTIFIER):
            return self.assignment()
        return self.expression_stmt()

    def var_stmt(self) -> VarStmt:
        name = self.consume(TokenType.IDENTIFIER, "Attendu un identifiant après VAR")
        self.consume(TokenType.ASSIGN, "Attendu '=' après l'identifiant")
        initializer = self.expression()
        return VarStmt(name, initializer)

    def string_stmt(self) -> StringStmt:
        value = self.consume(TokenType.STRING, "Attendu une chaîne après STRING")
        return StringStmt(Literal(value.value))

    def stringln_stmt(self) -> StringLnStmt:
        value = self.consume(TokenType.STRING, "Attendu une chaîne après STRINGLN")
        return StringLnStmt(Literal(value.value))

    def delay_stmt(self) -> DelayStmt:
        value = self.consume(TokenType.NUMBER, "Attendu un nombre après DELAY")
        return DelayStmt(Literal(value.value))

    def if_stmt(self) -> IfStmt:
        condition = self.expression()
        self.consume(TokenType.THEN, "Attendu 'THEN'")
        then_block = self.block()

        else_if_blocks = []
        while self.match(TokenType.ELSE_IF):
            else_if_condition = self.expression()
            self.consume(TokenType.THEN, "Attendu 'THEN' après 'ELSE IF'")
            else_if_block = self.block()
            else_if_blocks.append(IfStmt(else_if_condition, else_if_block))

        else_block = []
        if self.match(TokenType.ELSE):
            else_block = self.block()
        self.consume(TokenType.END_IF, "Attendu 'END_IF'")

        return IfStmt(condition, then_block, else_if_blocks, else_block)

    def while_stmt(self) -> WhileStmt:
        condition = self.expression()
        body = self.block()
        self.consume(TokenType.END_WHILE, "Attendu 'END_WHILE'")
        return WhileStmt(condition, body)

    def assignment(self) -> VarStmt:
        name = self.previous()
        self.consume(TokenType.ASSIGN, "Attendu '=' après l'identifiant")
        value = self.expression()
        return VarStmt(name, value)

    def block(self) -> list[Stmt]:
        statements = []
        while (
            not self.check(TokenType.END_IF)
            and not self.check(TokenType.ELSE_IF)
            and not self.check(TokenType.ELSE)
            and not self.check(TokenType.END_WHILE)
            and not self.is_at_end()
        ):
            statements.append(self.statement())
        return statements

    def expression_stmt(self) -> ExpressionStmt:
        expr = self.expression()
        return ExpressionStmt(expr)

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(TokenType.OP_EQUAL, TokenType.OP_NOT_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(
            TokenType.OP_GREATER,
            TokenType.OP_LESS,
            TokenType.OP_GREATER_EQUAL,
            TokenType.OP_LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenType.OP_PLUS, TokenType.OP_MINUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(
            TokenType.OP_MULTIPLY, TokenType.OP_DIVIDE, TokenType.OP_MODULO
        ):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.OP_NOT, TokenType.OP_MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NUMBER):
            return Literal(self.previous().value)
        if self.match(TokenType.STRING):
            return Literal(self.previous().value)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Attendu ')' après l'expression")

        return expr

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
        return self.peek().type == TokenType.EOF

    def consume(self, type, message) -> Token:
        if self.check(type):
            return self.advance()
        raise SyntaxError(message, self.peek().line, self.peek().column)
