from enum import Enum

class TokenType(Enum):
    # Keywords
    LET = "let"
    PRINT = "print"
    # Identifiers and literals
    ID = "id"
    NUMBER = "number"
    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    # Punctuation
    LPAREN = "("
    RPAREN = ")"
    SEMI = ";"
    # End of file
    EOF = "eof"

# For convenience
LET = TokenType.LET
PRINT = TokenType.PRINT
ID = TokenType.ID
NUMBER = TokenType.NUMBER
ASSIGN = TokenType.ASSIGN
PLUS = TokenType.PLUS
MINUS = TokenType.MINUS
MUL = TokenType.MUL
DIV = TokenType.DIV
LPAREN = TokenType.LPAREN
RPAREN = TokenType.RPAREN
SEMI = TokenType.SEMI
EOF = TokenType.EOF

KEYWORDS = {
    "let": LET,
    "print": PRINT,
}

class Token:
    def __init__(self, type, lexeme, line, column):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.lexeme}', {self.line}, {self.column})"
