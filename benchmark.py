import timeit

def benchmark_lexer():
    setup = "from lexer import Lexer"
    stmt = """
lexer = Lexer('''
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
''')
tokens = list(lexer.tokenize())
    """
    while True:
        result = timeit.timeit(stmt, setup, number=1000)
        print(f"Average time per run: {result/1000:.6f} seconds")

benchmark_lexer()
