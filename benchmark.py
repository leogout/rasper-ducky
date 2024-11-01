import timeit


def benchmark_lexer():
    setup = """
from rasper_ducky.duckyscript.preprocessor import Preprocessor
from rasper_ducky.duckyscript.lexer import Lexer
"""
    stmt = """
code = '''
    RD_KBD WIN FR

    DEFINE #COUNT 3

    FUNCTION open_powershell()
        GUI R
        STRINGLN powershell
    END_FUNCTION

    FUNCTION hello_world()
        $x = 0
        WHILE ($x < #COUNT)
            DELAY 500
            STRING Hello, World!
            SPACE
            $x = $x + 1
        END_WHILE
    END_FUNCTION

    open_powershell()
    DELAY 1000
    hello_world()

    IF TRUE THEN
        IF FALSE THEN
            STRING A
        ELSE
            IF TRUE THEN
                STRING B
            ELSE
                STRING C
            END_IF
        END_IF
    END_IF
    DELAY 10
    VAR $x = 10
    STRINGLN Hello, World!
    FUNCTION f(x)
        STRING Coucou
    END_FUNCTION
    WHILE TRUE
        STRING Hello
    END_WHILE
'''
preprocessor = Preprocessor()
code = preprocessor.process(code)
lexer = Lexer(code)
tokens = list(lexer.tokenize())
"""
    iterations = 10000
    result = timeit.timeit(stmt, setup, number=iterations)
    print(f"Average time per run: {result/iterations:.6f} seconds")


benchmark_lexer()
