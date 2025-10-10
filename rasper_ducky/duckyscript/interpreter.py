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


class EvalTask:
    """Represents a task to evaluate an expression node"""
    def __init__(self, node):
        self.node = node


class BinaryOpTask:
    """Represents a binary operation waiting for its operands"""
    def __init__(self, operator, left_value=None):
        self.operator = operator
        self.left_value = left_value


class UnaryOpTask:
    """Represents a unary operation waiting for its operand"""
    def __init__(self, operator):
        self.operator = operator


class AssignTask:
    """Represents an assignment waiting for its value"""
    def __init__(self, var_name):
        self.var_name = var_name


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
        self.eval_stack = []
        self.value_stack = []
        self.stmt_stack = []

    def interpret(self, ast: list[Stmt]):
        """Stack-based interpreter to avoid recursion limits"""
        self.stmt_stack = list(reversed(ast))

        while self.stmt_stack:
            node = self.stmt_stack.pop()
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
            self._push_statements(node.then_block)
        else:
            self._execute_else_if_or_else(node)

    def _execute_else_if_or_else(self, node: IfStmt):
        for else_if in node.else_if_blocks:
            if self._evaluate(else_if.condition):
                self._push_statements(else_if.then_block)
                return
        self._push_statements(node.else_block)

    def _push_statements(self, statements: list[Stmt]):
        """Push statements onto execution stack in reverse order"""
        for statement in reversed(statements):
            self.stmt_stack.append(statement)

    def _execute_while_statement(self, node: WhileStmt):
        if self._evaluate(node.condition):
            self.stmt_stack.append(node)
            self._push_statements(node.body)

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
        self._push_statements(self.functions[node.name.value])

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
        """Stack-based expression evaluator to avoid recursion limits"""
        self.eval_stack = [EvalTask(node)]
        self.value_stack = []

        while self.eval_stack:
            task = self.eval_stack.pop()

            if isinstance(task, EvalTask):
                self._process_eval_task(task.node)
            elif isinstance(task, BinaryOpTask):
                self._process_binary_op(task)
            elif isinstance(task, UnaryOpTask):
                self._process_unary_op(task)
            elif isinstance(task, AssignTask):
                self._process_assign(task)

        return self.value_stack.pop() if self.value_stack else None

    def _process_eval_task(self, node: Expr):
        """Process an evaluation task by pushing work onto stacks"""
        if isinstance(node, Literal):
            self.value_stack.append(int(node.value))

        elif isinstance(node, Variable):
            try:
                self.value_stack.append(self.variables[node.name.value])
            except KeyError:
                raise RuntimeError(f"Undefined variable: {node.name.value}")

        elif isinstance(node, Binary):
            self.eval_stack.append(BinaryOpTask(node.operator))
            self.eval_stack.append(EvalTask(node.right))
            self.eval_stack.append(EvalTask(node.left))

        elif isinstance(node, Unary):
            self.eval_stack.append(UnaryOpTask(node.operator))
            self.eval_stack.append(EvalTask(node.right))

        elif isinstance(node, Grouping):
            self.eval_stack.append(EvalTask(node.expression))

        elif isinstance(node, Assign):
            self.eval_stack.append(AssignTask(node.name.value))
            self.eval_stack.append(EvalTask(node.value))

        elif isinstance(node, Call):
            self._execute_function_call(node)
            self.value_stack.append(None)

        else:
            raise RuntimeError(f"Unknown node type for evaluation: {type(node)}")

    def _process_binary_op(self, task: BinaryOpTask):
        """Process a binary operation with its two operands from value stack"""
        right = self.value_stack.pop()
        left = self.value_stack.pop()
        result = self._apply_operator(task.operator, left, right)
        self.value_stack.append(result)

    def _process_unary_op(self, task: UnaryOpTask):
        """Process a unary operation with its operand from value stack"""
        value = self.value_stack.pop()
        result = self._apply_unary_operator(task.operator, value)
        self.value_stack.append(result)

    def _process_assign(self, task: AssignTask):
        """Process an assignment with its value from value stack"""
        value = self.value_stack.pop()
        self.variables[task.var_name] = value
        self.value_stack.append(value)

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
