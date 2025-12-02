from lexer.tokens import *

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VarDecl(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Assign(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class PrintStmt(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.errors = []

    def parse(self):
        statements = []
        while not self.is_at_end():
            try:
                stmt = self.statement()
                if stmt:
                    statements.append(stmt)
            except Exception as e:
                self.errors.append(str(e))
                self.synchronize()
        return Program(statements), self.errors

    def is_at_end(self):
        return self.peek().type == EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise Exception(message)

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == SEMI:
                return
            if self.peek().type in [LET, PRINT, ID]:
                return
            self.advance()

    def statement(self):
        if self.match(LET):
            return self.var_decl()
        elif self.match(PRINT):
            return self.print_stmt()
        elif self.check(ID):
            return self.assign()
        return None

    def end_stmt(self, context):
        if self.match(SEMI):
            return
        if self.is_at_end():
            return
        if self.peek().type in [LET, PRINT, ID]:
            return
        raise Exception(f"Expect ';' after {context}.")

    def var_decl(self):
        name = self.consume(ID, "Expect variable name.").lexeme
        self.consume(ASSIGN, "Expect '=' after variable name.")
        expr = self.expression()
        self.end_stmt("variable declaration")
        return VarDecl(name, expr)

    def assign(self):
        name = self.consume(ID, "Expect variable name.").lexeme
        self.consume(ASSIGN, "Expect '=' after variable name.")
        expr = self.expression()
        self.end_stmt("assignment")
        return Assign(name, expr)

    def print_stmt(self):
        self.consume(LPAREN, "Expect '(' after 'print'.")
        expr = self.expression()
        self.consume(RPAREN, "Expect ')' after expression.")
        self.end_stmt("print statement")
        return PrintStmt(expr)

    def expression(self):
        expr = self.term()
        while self.match(PLUS, MINUS):
            op = self.previous()
            right = self.term()
            expr = BinaryOp(expr, op, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(MUL, DIV):
            op = self.previous()
            right = self.factor()
            expr = BinaryOp(expr, op, right)
        return expr

    def factor(self):
        if self.match(MINUS):
            op = self.previous()
            expr = self.factor()
            return UnaryOp(op, expr)
        elif self.match(LPAREN):
            expr = self.expression()
            self.consume(RPAREN, "Expect ')' after expression.")
            return expr
        elif self.match(NUMBER):
            return Number(float(self.previous().lexeme))
        elif self.match(ID):
            return Identifier(self.previous().lexeme)
        raise Exception("Expect expression.")

    def print_tree(self, node, indent=0):
        prefix = "  " * indent
        if isinstance(node, Program):
            print(f"{prefix}Program")
            for stmt in node.statements:
                self.print_tree(stmt, indent + 1)
        elif isinstance(node, VarDecl):
            print(f"{prefix}VarDecl")
            print(f"{prefix}  ID '{node.name}'")
            print(f"{prefix}  ASSIGN '='")
            self.print_tree(node.expr, indent + 2)
            print(f"{prefix}  SEMI ';'")
        elif isinstance(node, Assign):
            print(f"{prefix}Assign")
            print(f"{prefix}  ID '{node.name}'")
            print(f"{prefix}  ASSIGN '='")
            self.print_tree(node.expr, indent + 2)
            print(f"{prefix}  SEMI ';'")
        elif isinstance(node, PrintStmt):
            print(f"{prefix}PrintStmt")
            print(f"{prefix}  PRINT 'print'")
            print(f"{prefix}  LPAREN '('")
            self.print_tree(node.expr, indent + 2)
            print(f"{prefix}  RPAREN ')'")
            print(f"{prefix}  SEMI ';'")
        elif isinstance(node, BinaryOp):
            print(f"{prefix}BinaryOp")
            self.print_tree(node.left, indent + 1)
            print(f"{prefix}  {node.op.type.name} '{node.op.lexeme}'")
            self.print_tree(node.right, indent + 1)
        elif isinstance(node, UnaryOp):
            print(f"{prefix}UnaryOp")
            print(f"{prefix}  {node.op.type.name} '{node.op.lexeme}'")
            self.print_tree(node.expr, indent + 1)
        elif isinstance(node, Number):
            print(f"{prefix}Number '{node.value}'")
        elif isinstance(node, Identifier):
            print(f"{prefix}ID '{node.name}'")
