from preprocessor import Preprocessor
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

class Compiler:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.lexer = Lexer()

    def compile(self, code):
        preprocessed_code = self.preprocessor.process(code)
        return list(self.lexer.tokenize(preprocessed_code))



# Utilisation
if __name__ == "__main__":
    
#     code = """
# DEFINE MAX_VALUE 100
# VAR $x = MAX_VALUE
# DELAY $x * 2 + 5


# STRING Hello, World!
# VAR $spam = 5
#     """
    code = """
    DEFINE MAX_VALUE 100
    VAR $x = MAX_VALUE
    VAR $y = $x * 2 + 5
    VAR $z = $y + $x + 10
    VAR $a = $z + $y / 3 + $x * 10
    VAR $c = 12 + 3

    STRING Hello, World!
    VAR $spam = 5
"""

    compiler = Compiler()
    tokens = compiler.compile(code)
    
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    ast = parser.parse()
    
    for node in ast:
        print(node)

    interpreter = Interpreter()
    interpreter.interpret(ast)

    print(interpreter.variables)
