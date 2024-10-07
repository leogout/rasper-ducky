from dataclasses import dataclass
from lexer import TokenType, Token

class ASTNode:
    pass

@dataclass
class VarNode(ASTNode):
    name: str
    __repr__ = lambda self: f"VAR({self.name})"

@dataclass
class VarDeclarationNode(ASTNode):
    name: str
    value: ASTNode
    __repr__ = lambda self: f"VAR_DECL({self.name}, {self.value})"

@dataclass
class StringNode(ASTNode):
    value: str
    __repr__ = lambda self: f"STR({self.value})"

@dataclass
class PrintStringNode(ASTNode):
    value: StringNode
    __repr__ = lambda self: f"PRINT_STR({self.value})"

@dataclass
class NumberNode(ASTNode):
    value: int
    __repr__ = lambda self: f"NUM({self.value})"

@dataclass
class OperatorNode(ASTNode):
    value: str
    __repr__ = lambda self: f"OP({self.value})"

@dataclass
class ExpressionNode(ASTNode):
    left: ASTNode
    operator: OperatorNode
    right: ASTNode
    __repr__ = lambda self: f"EXPR({self.left}, {self.operator}, {self.right})"

@dataclass
class IfStatementNode(ASTNode):
    condition: ExpressionNode
    then_block: list[ASTNode]
    __repr__ = lambda self: f"IF({self.condition}, {self.then_block})"

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
            name = self.consume(TokenType.ID, "Attendu un identifiant après VAR")
            self.consume(TokenType.ASSIGN, "Attendu '=' après l'identifiant")
            initializer = self.expression()
            return VarDeclarationNode(name.value, initializer)
        elif self.match(TokenType.PRINTSTRING):
            value = self.consume(TokenType.STRING, "Attendu une chaîne après STRING")
            return PrintStringNode(StringNode(value.value))
        elif self.match(TokenType.IF):
            condition = self.expression()
            self.consume(TokenType.THEN, "Attendu 'THEN'")
            then_branch = []
            while not self.check(TokenType.END_IF):
                then_branch.append(self.statement())
            self.consume(TokenType.END_IF, "Attendu 'END_IF'")
            return IfStatementNode(condition, then_branch)
        else:
            raise SyntaxError(f"Instruction inattendue à la ligne {self.peek().line}, colonne {self.peek().column}, token: {self.peek().value}")

    def expression(self) -> ExpressionNode:
        left = self.term()
        while self.match(TokenType.OP):
            operator = OperatorNode(self.previous().value)
            right = self.term()
            left = ExpressionNode(left, operator, right)
        return left

    def term(self) -> ASTNode:
        if self.match(TokenType.ID):
            return VarNode(self.previous().value)
        elif self.match(TokenType.NUMBER):
            return NumberNode(self.previous().value)
        
        raise SyntaxError("Expression attendue")

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
