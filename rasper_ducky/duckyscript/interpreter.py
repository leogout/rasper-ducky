import random
import time

from .keyboard import RasperDuckyKeyboard
from .parser import (
    KeyPressStmt,
    RandomCharStmt,
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
    Tok,
    StringLnStmt,
    DelayStmt,
    FunctionStmt,
    Stmt,
    ExpressionStmt,
    Assign,
    Call,
    KbdStmt,
    RandomCharFromStmt,
)


class Interpreter:
    BINARY_OPERATORS = {
        Tok.OP_PLUS: lambda l, r: l + r,
        Tok.OP_MINUS: lambda l, r: l - r,
        Tok.OP_MULTIPLY: lambda l, r: l * r,
        Tok.OP_DIVIDE: lambda l, r: l / r,
        Tok.OP_LESS: lambda l, r: l < r,
        Tok.OP_GREATER: lambda l, r: l > r,
        Tok.OP_LESS_EQUAL: lambda l, r: l <= r,
        Tok.OP_GREATER_EQUAL: lambda l, r: l >= r,
        Tok.OP_EQUAL: lambda l, r: l == r,
        Tok.OP_NOT_EQUAL: lambda l, r: l != r,
        Tok.OP_AND: lambda l, r: l and r,
        Tok.OP_OR: lambda l, r: l or r,
        Tok.OP_BITWISE_AND: lambda l, r: l & r,
        Tok.OP_BITWISE_OR: lambda l, r: l | r,
        Tok.OP_SHIFT_LEFT: lambda l, r: l << r,
        Tok.OP_SHIFT_RIGHT: lambda l, r: l >> r,
    }

    UNARY_OPERATORS = {
        Tok.OP_MINUS: lambda l: -l,
        Tok.OP_PLUS: lambda l: l,
        Tok.OP_NOT: lambda l: not l,
    }

    RANDOM_CHAR_SETS = {
        "RANDOM_LOWERCASE_LETTER": "abcdefghijklmnopqrstuvwxyz",
        "RANDOM_UPPERCASE_LETTER": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "RANDOM_LETTER": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "RANDOM_NUMBER": "0123456789",
        "RANDOM_SPECIAL": "!@#$%^&*()",
        "RANDOM_CHAR": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()",
    }

    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.execution_stack = []
        self.keyboard = RasperDuckyKeyboard("win", "uk")

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
        elif isinstance(node, FunctionStmt):
            self._execute_function_declaration(node)
        elif isinstance(node, KeyPressStmt):
            self._execute_keypress(node)
        elif isinstance(node, KbdStmt):
            self._execute_kbd(node)
        elif isinstance(node, ExpressionStmt):
            self._execute_expression(node.expression)
        elif isinstance(node, RandomCharStmt):
            self._execute_random_char(node)
        elif isinstance(node, RandomCharFromStmt):
            self._execute_random_char_from(node)
        elif isinstance(node, Literal):
            pass  # A literal is a value, nothing to execute
        else:
            raise RuntimeError(f"Unknown node type: {type(node)}")

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
        self.keyboard.type_string(node.value.value)

    def _execute_print_stringln(self, node: StringLnStmt):
        self.execution_stack.append(node.value.value)
        self.keyboard.type_string(node.value.value)
        self.keyboard.press_key("ENTER")
        self.keyboard.release_all()

    def _execute_delay(self, node: DelayStmt):
        time.sleep(float(node.value.value) / 1000)

    def _execute_expression(self, node: Expr):
        self._evaluate(node)

    def _execute_function_declaration(self, node: FunctionStmt):
        self.functions[node.name.value] = node.body

    def _execute_function_call(self, node: Call):
        self._execute_block(self.functions[node.name.value])

    def _execute_keypress(self, node: KeyPressStmt):
        if node.release:
            for key in node.keys:
                self.keyboard.release_key(key.value)
        else:
            for key in node.keys:
                self.keyboard.press_key(key.value)

        if not node.hold and not node.release:
            self.keyboard.release_all()

    def _execute_kbd(self, node: KbdStmt):
        self.keyboard = RasperDuckyKeyboard(
            node.platform.value.lower(), node.language.value.lower()
        )

    def _execute_random_char(self, node: RandomCharStmt):
        if node.type.value not in self.RANDOM_CHAR_SETS:
            raise RuntimeError(f"Unknown random character set: {node.type.value}")
        char_set = self.RANDOM_CHAR_SETS[node.type.value]
        self.keyboard.type_string(random.choice(char_set))

    def _execute_random_char_from(self, node: RandomCharFromStmt):
        self.keyboard.type_string(random.choice(str(node.value.value)))

    def _evaluate(self, node: Expr):
        if isinstance(node, Binary):
            return self._evaluate_expression(node)
        elif isinstance(node, Unary):
            return self._evaluate_unary(node)
        elif isinstance(node, Literal):
            return int(node.value)
        elif isinstance(node, Variable):
            try:
                return self.variables[node.name.value]
            except KeyError:
                raise RuntimeError(f"Undefined variable: {node.name.value}")
        elif isinstance(node, Assign):
            value = self._evaluate(node.value)
            self.variables[node.name.value] = value
            return value
        elif isinstance(node, Grouping):
            return self._evaluate(node.expression)
        elif isinstance(node, Call):
            return self._execute_function_call(node)
        else:
            raise RuntimeError(f"Unknown node type for evaluation: {type(node)}")

    def _evaluate_expression(self, node: Binary):
        left = self._evaluate(node.left)
        right = self._evaluate(node.right)
        return self._apply_operator(node.operator, left, right)

    def _evaluate_unary(self, node: Unary):
        value = self._evaluate(node.right)
        return self._apply_unary_operator(node.operator, value)

    def _apply_operator(self, operator: Token, left, right):
        if operator.type in self.BINARY_OPERATORS:
            return self.BINARY_OPERATORS[operator.type](left, right)
        elif operator.value == "=":
            return right
        else:
            raise RuntimeError(f"Unknown operator: {operator.value}")

    def _apply_unary_operator(self, operator: Token, value):
        if operator.type in self.UNARY_OPERATORS:
            return self.UNARY_OPERATORS[operator.type](value)
        else:
            raise RuntimeError(f"Unknown operator: {operator.value}")
