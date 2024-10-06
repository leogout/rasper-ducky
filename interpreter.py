from parser import VarDeclarationNode, ExpressionNode, NumberNode, VarNode, PrintStringNode, OperatorNode

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.definitions = {}
        self.execution_stack = []

    def interpret(self, ast):
        for node in ast:
            self.execute(node)

    def execute(self, node):
        print("execute", node)
        if isinstance(node, VarDeclarationNode):
            value = self.evaluate(node.value)
            self.variables[node.name] = value
        elif isinstance(node, PrintStringNode):
            self.execution_stack.append(node.value.value)
        else:
            raise RuntimeError(f"Type de noeud inconnu : {type(node)}")

    def evaluate(self, node):
        print("evaluate", node)
        if isinstance(node, ExpressionNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            return self.apply_operator(node.operator, left, right)
        elif isinstance(node, NumberNode):
            return int(node.value)
        elif isinstance(node, VarNode):
            return self.variables[node.name]
        else:
            raise RuntimeError(f"Type de noeud inconnu pour l'évaluation : {type(node)}")

    def apply_operator(self, operator: OperatorNode, left, right):
        if operator.value == '+':
            return left + right
        elif operator.value == '-':
            return left - right
        elif operator.value == '*':
            return left * right
        elif operator.value == '/':
            return left / right
        else:
            raise RuntimeError(f"Opérateur inconnu : {operator.value}")