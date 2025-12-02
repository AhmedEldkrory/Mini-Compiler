from parser.parser import Program, VarDecl, Assign, PrintStmt, BinaryOp, UnaryOp, Number, Identifier

class SemanticAnalyzer:
    def __init__(self):
        self.errors = []
        self.symbols = {}

    def analyze(self, ast):
        self.errors = []
        self.symbols = {}
        self.visit_program(ast)
        return self.errors

    def visit_program(self, node):
        for stmt in node.statements:
            self.visit_statement(stmt)

    def visit_statement(self, node):
        if isinstance(node, VarDecl):
            if node.name in self.symbols:
                self.errors.append(f"Variable '{node.name}' already declared.")
            self.symbols.setdefault(node.name, "number")
            self.visit_expression(node.expr)
        elif isinstance(node, Assign):
            if node.name not in self.symbols:
                self.errors.append(f"Variable '{node.name}' not declared.")
            self.visit_expression(node.expr)
        elif isinstance(node, PrintStmt):
            self.visit_expression(node.expr)

    def visit_expression(self, node):
        if isinstance(node, BinaryOp):
            self.visit_expression(node.left)
            self.visit_expression(node.right)
        elif isinstance(node, UnaryOp):
            self.visit_expression(node.expr)
        elif isinstance(node, Number):
            return
        elif isinstance(node, Identifier):
            if node.name not in self.symbols:
                self.errors.append(f"Variable '{node.name}' not declared.")
        else:
            self.errors.append("Invalid expression.")
