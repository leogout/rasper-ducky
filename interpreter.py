import operator as op
from parser import VarDeclarationNode, ExpressionNode, NumberNode, VarNode, PrintStringNode, OperatorNode, IfStatementNode

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.execution_stack = []

    def interpret(self, ast):
        for node in ast:
            self._execute(node)

    def _execute(self, node):
        if isinstance(node, VarDeclarationNode):
            self._execute_var_declaration(node)
        elif isinstance(node, IfStatementNode):
            self._execute_if_statement(node)
        elif isinstance(node, PrintStringNode):
            self._execute_print_string(node)
        elif isinstance(node, ExpressionNode):
            self._execute_expression(node)
        else:
            raise RuntimeError(f"Type de noeud inconnu : {type(node)}")

    def _execute_var_declaration(self, node):
        value = self._evaluate(node.value)
        self.variables[node.name] = value

    def _execute_if_statement(self, node):
        if self._evaluate(node.condition):
            self._execute_block(node.then_block)
        else:
            self._execute_else_if_or_else(node)

    def _execute_else_if_or_else(self, node):
        for else_if in node.else_if_blocks:
            if self._evaluate(else_if.condition):
                self._execute_block(else_if.then_block)
                return
        self._execute_block(node.else_block)
    
    def _execute_block(self, block):
        for statement in block:
            self._execute(statement)

    def _execute_print_string(self, node):
        self.execution_stack.append(node.value.value)

    def _execute_expression(self, node):
        self._evaluate(node)

    def _evaluate(self, node):
        if isinstance(node, ExpressionNode):
            return self._evaluate_expression(node)
        elif isinstance(node, NumberNode):
            return int(node.value)
        elif isinstance(node, VarNode):
            try:
                return self.variables[node.name]
            except KeyError:
                raise RuntimeError(f"Variable non définie : {node.name}")
        else:
            raise RuntimeError(f"Type de noeud inconnu pour l'évaluation : {type(node)}")

    def _evaluate_expression(self, node):
        left = self._evaluate(node.left)
        right = self._evaluate(node.right)
        return self._apply_operator(node.operator, left, right)

    def _apply_operator(self, operator: OperatorNode, left, right):
        operators = {
            '+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.truediv,
            '<': op.lt,
            '>': op.gt,
            '<=': op.le,
            '>=': op.ge,
            '==': op.eq,
            '!=': op.ne,
            '&&': lambda l, r: l and r,
            '||': lambda l, r: l or r,
            '&': op.and_,
            '|': op.or_,
            '<<': op.lshift,
            '>>': op.rshift
        }

        if operator.value in operators:
            return operators[operator.value](left, right)
        else:
            raise RuntimeError(f"Opérateur inconnu : {operator.value}")