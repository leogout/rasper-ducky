import operator as op
import time
from parser import (
    VarStmt,
    Binary,
    Unary,
    Literal,
    Grouping,
    Variable,
    StringStmt,
    IfStmt,
    WhileStmt,
    Expr,
    Token,
    TokenType,
    StringLnStmt,
    DelayStmt,
    Stmt,
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

    def interpret(self, ast: list[Stmt]):
        for node in ast:
            self._execute(node)

    def _execute(self, node: Stmt):
        if isinstance(node, VarStmt):
            self._execute_var_declaration(node)
        elif isinstance(node, IfStmt):
            self._execute_if_statement(node)
        elif isinstance(node, WhileStmt):
            self._execute_while_statement(node)
        elif isinstance(node, StringStmt):
            self._execute_print_string(node)
        elif isinstance(node, StringLnStmt):
            self._execute_print_stringln(node)
        elif isinstance(node, DelayStmt):
            self._execute_delay(node)
        elif isinstance(node, Binary):
            self._execute_expression(node)
        elif isinstance(node, Literal):
            pass  # A literal is a value, nothing to execute
        else:
            raise RuntimeError(f"Type de noeud inconnu : {type(node)}")

    def _execute_var_declaration(self, node: VarStmt):
        value = self._evaluate(node.value)
        self.variables[node.name.value] = value

    def _execute_if_statement(self, node: IfStmt):
        if self._evaluate(node.condition):
            self._execute_block(node.then_block)
        else:
            self._execute_else_if_or_else(node)

    def _execute_else_if_or_else(self, node: IfStmt):
        for else_if in node.else_if_blocks:
            if self._evaluate(else_if.condition):
                self._execute_block(else_if.then_block)
                return
        self._execute_block(node.else_block)

    def _execute_block(self, block: list[Stmt]):
        for statement in block:
            self._execute(statement)

    def _execute_while_statement(self, node: WhileStmt):
        while self._evaluate(node.condition):
            self._execute_block(node.body)

    def _execute_print_string(self, node: StringStmt):
        self.execution_stack.append(node.value.value)

    def _execute_print_stringln(self, node: StringLnStmt):
        self.execution_stack.append(node.value.value)

    def _execute_delay(self, node: DelayStmt):
        time.sleep(int(node.value.value))

    def _execute_expression(self, node: Binary):
        self._evaluate(node)

    def _evaluate(self, node: Expr):
        if isinstance(node, Binary):
            return self._evaluate_expression(node)
        elif isinstance(node, Literal):
            return int(node.value)
        elif isinstance(node, Variable):
            try:
                return self.variables[node.name.value]
            except KeyError:
                raise RuntimeError(f"Variable non définie : {node.name.value}")
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
