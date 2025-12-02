from parser.parser import *

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.environment = {}

    def interpret(self):
        try:
            self.visit_program(self.ast)
            return "Interpretation successful."
        except Exception as e:
            return f"Runtime error: {str(e)}"

    def visit_program(self, node):
        for stmt in node.statements:
            self.visit_statement(stmt)

    def visit_statement(self, node):
        if isinstance(node, VarDecl):
            value = self.visit_expression(node.expr)
            self.environment[node.name] = value
        elif isinstance(node, Assign):
            value = self.visit_expression(node.expr)
            if node.name not in self.environment:
                raise Exception(f"Variable '{node.name}' not declared.")
            self.environment[node.name] = value
        elif isinstance(node, PrintStmt):
            value = self.visit_expression(node.expr)
            print(value)

    def visit_expression(self, node):
        if isinstance(node, BinaryOp):
            left = self.visit_expression(node.left)
            right = self.visit_expression(node.right)
            if node.op.type == PLUS:
                return left + right
            elif node.op.type == MINUS:
                return left - right
            elif node.op.type == MUL:
                return left * right
            elif node.op.type == DIV:
                if right == 0:
                    raise Exception("Division by zero.")
                return left / right
        elif isinstance(node, UnaryOp):
            expr = self.visit_expression(node.expr)
            if node.op.type == MINUS:
                return -expr
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, Identifier):
            if node.name not in self.environment:
                raise Exception(f"Variable '{node.name}' not declared.")
            return self.environment[node.name]
        raise Exception("Invalid expression.")
