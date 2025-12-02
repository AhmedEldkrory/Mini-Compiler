import re
from lexer.tokens import Token, LET, PRINT, ID, NUMBER, ASSIGN, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, SEMI, EOF, KEYWORDS

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.errors = []

    def tokenize(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(EOF, "", self.line, self.column))
        return self.tokens, self.errors

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        self.column += 1
        return self.source[self.current - 1]

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def add_token(self, type):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, self.line, self.column - len(text)))

    def scan_token(self):
        c = self.advance()
        if c == '(':
            self.add_token(LPAREN)
        elif c == ')':
            self.add_token(RPAREN)
        elif c == '+':
            self.add_token(PLUS)
        elif c == '-':
            self.add_token(MINUS)
        elif c == '*':
            self.add_token(MUL)
        elif c == '/':
            self.add_token(DIV)
        elif c == '=':
            self.add_token(ASSIGN)
        elif c == ';':
            self.add_token(SEMI)
        elif c == ' ' or c == '\r' or c == '\t':
            pass  # Ignore whitespace
        elif c == '\n':
            self.line += 1
            self.column = 1
        elif c.isdigit():
            self.number()
        elif c.isalpha():
            self.identifier()
        else:
            self.errors.append(f"Unexpected character '{c}' at line {self.line}, col {self.column - 1}")

    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.add_token(NUMBER)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        type = KEYWORDS.get(text, ID)
        self.add_token(type)
