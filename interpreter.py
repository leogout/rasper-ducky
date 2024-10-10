import operator as op
from parser import (
    VarDeclarationNode,
    Binary,
    Unary,
    Literal,
    Grouping,
    VarNode,
    PrintStringNode,
    IfStatementNode,
    WhileStatementNode,
    ASTNode,
    Token,
    TokenType,
)


class Interpreter:
    OPERATORS = operators = {
        TokenType.OP_PLUS: op.add,
        TokenType.OP_MINUS: op.sub,
        TokenType.OP_MULTIPLY: op.mul,
        TokenType.OP_DIVIDE: op.truediv,
        TokenType.OP_LESS: op.lt,
        TokenType.OP_GREATER: op.gt,
        TokenType.OP_LESS_EQUAL: op.le,
        TokenType.OP_GREATER_EQUAL: op.ge,
        TokenType.OP_EQUAL: op.eq,
        TokenType.OP_NOT_EQUAL: op.ne,
        TokenType.OP_AND: lambda l, r: l and r,
        TokenType.OP_OR: lambda l, r: l or r,
        TokenType.OP_BITWISE_AND: op.and_,
        TokenType.OP_BITWISE_OR: op.or_,
        TokenType.OP_SHIFT_LEFT: op.lshift,
        TokenType.OP_SHIFT_RIGHT: op.rshift,
    }

    def __init__(self):
        self.variables = {}
        self.execution_stack = []

    def interpret(self, ast: list[ASTNode]):
        for node in ast:
            self._execute(node)

    def _execute(self, node: ASTNode):
        if isinstance(node, VarDeclarationNode):
            self._execute_var_declaration(node)
        elif isinstance(node, IfStatementNode):
            self._execute_if_statement(node)
        elif isinstance(node, WhileStatementNode):
            self._execute_while_statement(node)
        elif isinstance(node, PrintStringNode):
            self._execute_print_string(node)
        elif isinstance(node, Binary):
            self._execute_expression(node)
        else:
            raise RuntimeError(f"Type de noeud inconnu : {type(node)}")

    def _execute_var_declaration(self, node: VarDeclarationNode):
        value = self._evaluate(node.value)
        self.variables[node.name] = value

    def _execute_if_statement(self, node: IfStatementNode):
        if self._evaluate(node.condition):
            self._execute_block(node.then_block)
        else:
            self._execute_else_if_or_else(node)

    def _execute_else_if_or_else(self, node: IfStatementNode):
        for else_if in node.else_if_blocks:
            if self._evaluate(else_if.condition):
                self._execute_block(else_if.then_block)
                return
        self._execute_block(node.else_block)

    def _execute_block(self, block: list[ASTNode]):
        for statement in block:
            self._execute(statement)

    def _execute_while_statement(self, node: WhileStatementNode):
        while self._evaluate(node.condition):
            self._execute_block(node.body)

    def _execute_print_string(self, node: PrintStringNode):
        self.execution_stack.append(node.value.value)

    def _execute_expression(self, node: Binary):
        self._evaluate(node)

    def _evaluate(self, node: ASTNode):
        if isinstance(node, Binary):
            return self._evaluate_expression(node)
        elif isinstance(node, Literal):
            return int(node.value)
        elif isinstance(node, VarNode):
            try:
                return self.variables[node.name]
            except KeyError:
                raise RuntimeError(f"Variable non définie : {node.name}")
        else:
            raise RuntimeError(
                f"Type de noeud inconnu pour l'évaluation : {type(node)}"
            )

    def _evaluate_expression(self, node: Binary):
        left = self._evaluate(node.left)
        right = self._evaluate(node.right)
        return self._apply_operator(node.operator, left, right)

    def _apply_operator(self, operator: Token, left, right):

        if operator.type in self.OPERATORS:
            return self.OPERATORS[operator.type](left, right)
        elif operator.value == "=":
            return right
        else:
            raise RuntimeError(f"Opérateur inconnu : {operator.value}")
