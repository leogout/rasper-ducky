import time

from rasper_ducky.interpreter.lexer import Lexer
from rasper_ducky.interpreter.parser import Parser
from rasper_ducky.interpreter.interpreter import Interpreter
from rasper_ducky.interpreter.preprocessor import Preprocessor

# sleep at the start to allow the device to be recognized by the host computer
time.sleep(.5)


def execute(code: str):
    preprocessor = Preprocessor()
    code = preprocessor.process(code)
    lexer = Lexer()
    tokens = list(lexer.tokenize(code))
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)


with open("payload.dd", "r") as file:
    payload_code = file.read()

execute(payload_code)
