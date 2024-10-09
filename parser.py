from dataclasses import dataclass, field
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
    else_if_blocks: list['IfStatementNode'] = field(default_factory=list)
    else_block: list[ASTNode] = field(default_factory=list)
    __repr__ = lambda self: f"IF({self.condition}, {self.then_block}, {self.else_if_blocks}, {self.else_block})"

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
        elif self.match(TokenType.IF):
            return self.if_statement()
        else:
            raise SyntaxError(f"Instruction inattendue à la ligne {self.peek().line}, colonne {self.peek().column}, token: {self.peek().value}")

    def var_declaration(self) -> VarDeclarationNode:
        name = self.consume(TokenType.ID, "Attendu un identifiant après VAR")
        self.consume(TokenType.ASSIGN, "Attendu '=' après l'identifiant")
        initializer = self.expression()
        return VarDeclarationNode(name.value, initializer)

    def print_string(self) -> PrintStringNode:
        value = self.consume(TokenType.STRING, "Attendu une chaîne après STRING")
        return PrintStringNode(StringNode(value.value))

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

    def block(self) -> list[ASTNode]:
        statements = []
        while not self.check(TokenType.END_IF) and not self.check(TokenType.ELSE_IF) and not self.check(TokenType.ELSE) and not self.is_at_end():
            statements.append(self.statement())
        return statements

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


if __name__ == "__main__":

    tokens = [
        Token(TokenType.IF, 'IF', 1, 0),
        Token(TokenType.ID, '$x', 1, 3),
        Token(TokenType.OP, '>', 1, 6),
        Token(TokenType.NUMBER, '0', 1, 8),
        Token(TokenType.THEN, 'THEN', 1, 10),
        Token(TokenType.VAR, 'VAR', 2, 0),
        Token(TokenType.ID, '$y', 2, 4),
        Token(TokenType.ASSIGN, '=', 2, 7),
        Token(TokenType.NUMBER, '1', 2, 9),
        Token(TokenType.ELSE, 'ELSE', 3, 0),
        Token(TokenType.PRINTSTRING, 'STRING', 4, 0),
        Token(TokenType.STRING, 'Hey there!', 4, 8),
        Token(TokenType.END_IF, 'END_IF', 5, 0),
        Token(TokenType.EOF, '', 5, 7)
    ]
    parser = Parser(tokens)
    ast = parser.parse()
    expected_ast = [
        IfStatementNode(
            ExpressionNode(VarNode("$x"), OperatorNode('>'), NumberNode('0')),
            [VarDeclarationNode("$y", NumberNode('1'))],
            [PrintStringNode(StringNode('Hey there!'))]
        )
    ]
