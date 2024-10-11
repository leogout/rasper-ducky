from dataclasses import dataclass, field
from lexer import TokenType, Token


class ASTNode:
    pass


@dataclass
class VarNode(ASTNode):
    name: str

    def __repr__(self):
        return f"VAR({self.name})"


@dataclass
class VarDeclarationNode(ASTNode):
    name: str
    value: ASTNode

    def __repr__(self):
        return f"VAR_DECL({self.name}, {self.value})"


@dataclass
class Binary(ASTNode):
    left: ASTNode
    operator: Token
    right: ASTNode

    def __repr__(self):
        return f"EXPR({self.left}, {self.operator.value}, {self.right})"


@dataclass
class Unary(ASTNode):
    operator: Token
    right: ASTNode

    def __repr__(self):
        return f"EXPR({self.operator.value}, {self.right})"


@dataclass
class Literal(ASTNode):
    value: bool | int | str

    def __repr__(self):
        return f"LITERAL({self.value})"


@dataclass
class Grouping(ASTNode):
    expression: ASTNode

    def __repr__(self):
        return f"GROUP({self.expression})"


@dataclass
class DelayNode(ASTNode):
    value: Literal

    def __repr__(self):
        return f"DELAY({self.value})"


@dataclass
class PrintStringNode(ASTNode):
    value: Literal

    def __repr__(self):
        return f"PRINT_STR({self.value})"


@dataclass
class PrintStringLnNode(ASTNode):
    value: Literal

    def __repr__(self):
        return f"PRINT_STRLN({self.value})"


@dataclass
class IfStatementNode(ASTNode):
    condition: ASTNode
    then_block: list[ASTNode]
    else_if_blocks: list["IfStatementNode"] = field(default_factory=list)
    else_block: list[ASTNode] = field(default_factory=list)

    def __repr__(self):
        return f"IF({self.condition}, {self.then_block}, {self.else_if_blocks}, {self.else_block})"


@dataclass
class WhileStatementNode(ASTNode):
    condition: ASTNode
    body: list[ASTNode]

    def __repr__(self):
        return f"WHILE({self.condition}, {self.body})"


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[ASTNode]:
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return statements

    def statement(self) -> ASTNode:
        if self.match(TokenType.VAR):
            return self.var_declaration()
        elif self.match(TokenType.PRINTSTRING):
            return self.print_string()
        elif self.match(TokenType.PRINTSTRINGLN):
            return self.print_stringln()
        elif self.match(TokenType.DELAY):
            return self.delay()
        elif self.match(TokenType.IF):
            return self.if_statement()
        elif self.match(TokenType.WHILE):
            return self.while_statement()
        elif self.match(TokenType.ID):
            return self.assignment()
        return self.expression()

    def var_declaration(self) -> VarDeclarationNode:
        name = self.consume(TokenType.ID, "Attendu un identifiant après VAR")
        self.consume(TokenType.ASSIGN, "Attendu '=' après l'identifiant")
        initializer = self.expression()
        return VarDeclarationNode(name.value, initializer)

    def print_string(self) -> PrintStringNode:
        value = self.consume(TokenType.STRING, "Attendu une chaîne après STRING")
        return PrintStringNode(Literal(value.value))

    def print_stringln(self) -> PrintStringLnNode:
        value = self.consume(TokenType.STRING, "Attendu une chaîne après STRINGLN")
        return PrintStringLnNode(Literal(value.value))

    def delay(self) -> DelayNode:
        value = self.consume(TokenType.NUMBER, "Attendu un nombre après DELAY")
        return DelayNode(Literal(value.value))

    def if_statement(self) -> IfStatementNode:
        condition = self.expression()
        self.consume(TokenType.THEN, "Attendu 'THEN'")
        then_block = self.block()

        else_if_blocks = []
        while self.match(TokenType.ELSE_IF):
            else_if_condition = self.expression()
            self.consume(TokenType.THEN, "Attendu 'THEN' après 'ELSE IF'")
            else_if_block = self.block()
            else_if_blocks.append(IfStatementNode(else_if_condition, else_if_block))

        else_block = []
        if self.match(TokenType.ELSE):
            else_block = self.block()
        self.consume(TokenType.END_IF, "Attendu 'END_IF'")

        return IfStatementNode(condition, then_block, else_if_blocks, else_block)

    def while_statement(self) -> WhileStatementNode:
        condition = self.expression()
        body = self.block()
        self.consume(TokenType.END_WHILE, "Attendu 'END_WHILE'")
        return WhileStatementNode(condition, body)

    def assignment(self) -> VarDeclarationNode:
        name = self.previous()
        self.consume(TokenType.ASSIGN, "Attendu '=' après l'identifiant")
        value = self.expression()
        return VarDeclarationNode(name.value, value)

    def block(self) -> list[ASTNode]:
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

    def expression(self) -> ASTNode:
        return self.equality()

    def equality(self) -> ASTNode:
        expr = self.comparison()
        while self.match(TokenType.OP_EQUAL, TokenType.OP_NOT_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
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

    def term(self):
        expr = self.factor()

        while self.match(TokenType.OP_PLUS, TokenType.OP_MINUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()

        while self.match(
            TokenType.OP_MULTIPLY, TokenType.OP_DIVIDE, TokenType.OP_MODULO
        ):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.OP_NOT, TokenType.OP_MINUS):
            operator = self.previous()
            right = self.unary()
            return Binary(operator, right)

        return self.primary()

    def primary(self) -> ASTNode:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NUMBER):
            return Literal(self.previous().value)
        if self.match(TokenType.STRING):
            return Literal(self.previous().value)
        if self.match(TokenType.ID):
            return VarNode(self.previous().value)

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
