from rasper_ducky.duckyscript.lexer import Token, Tok


class Lexer:
    KEYWORDS = {
        "VAR": Tok.VAR,
    }

    def __init__(self, code: str):
        self.code = code
        self.current = 0
        self.start = 0
        self.line = 1
        self.count = len(code)

    def is_end(self):
        return self.current >= self.count

    def advance(self):
        if not self.is_end():
            self.current += 1
        return self.code[self.current - 1]

    def peek(self):
        if not self.is_end():
            return self.code[self.current]
        return None

    def peek_next(self):
        if self.current + 1 >= self.count:
            return None
        return self.code[self.current + 1]

    def match(self, expected: str):
        if self.is_end():
            return False

        if self.peek() == expected:
            self.advance()
            return True
        return False

    def scan_tokens(self):
        while not self.is_end():
            self.start = self.current
            yield from self.scan_token()
        yield Token(Tok.EOL)
        yield Token(Tok.EOF)

    def is_digit(self, char: str):
        return not self.is_end() and char.isdigit()

    def is_alpha(self, char: str):
        return not self.is_end() and (char.isalpha() or char == "$")

    def is_alphanumeric(self, char: str):
        return self.is_digit(char) or self.is_alpha(char)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        yield Token(Tok.NUMBER, float(self.code[self.start : self.current]))

    def identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()

        identifier = self.code[self.start : self.current]
        keyword = self.KEYWORDS.get(identifier)
        if keyword is not None:
            yield Token(keyword, identifier)
        else:
            yield Token(Tok.IDENTIFIER, identifier)

    def scan_token(self):
        char = self.advance()
        print(char)

        if char == "(":
            yield Token(Tok.LPAREN)
        elif char == ")":
            yield Token(Tok.RPAREN)

        elif char == "=":
            yield Token(Tok.OP_EQUAL) if self.match("=") else Token(Tok.ASSIGN)
        elif char == "!":
            yield Token(Tok.OP_NOT_EQUAL) if self.match("=") else Token(Tok.OP_NOT)

        elif char == "\n":
            yield Token(Tok.EOL)
            self.line += 1

        elif self.is_digit(char):
            yield from self.number()

        elif self.is_alpha(char):
            yield from self.identifier()

        elif char == " ":
            pass
        else:
            raise Exception(f"Unexpected character: {char}")


if __name__ == "__main__":
    lexer = Lexer("VAR $val = 10\nVAR $val2 = 20")
    print(list(lexer.scan_tokens()))
