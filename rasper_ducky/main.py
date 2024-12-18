import time

from duckyscript.lexer import Lexer
from duckyscript.parser import Parser
from duckyscript.interpreter import Interpreter
from duckyscript.preprocessor import Preprocessor

# sleep at the start to allow the device to be recognized by the host computer
time.sleep(0.5)


def execute(code: str):
    preprocessor = Preprocessor()
    code = preprocessor.process(code)
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)


with open("payload.dd", "r") as file:
    payload_code = file.read()


execute(payload_code)
