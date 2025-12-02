# Mini Compiler Front-End Visualizer

A complete mini compiler front-end visualizer built in Python 3 for a university Compiler course. This project demonstrates the key phases of compilation: lexical analysis, syntax analysis, semantic analysis, and interpretation.

## Features

- **Lexical Analysis**: Tokenizes source code into tokens with error handling.
- **Syntax Analysis**: Recursive descent parser that builds and visualizes a parse tree.
- **Semantic Analysis**: Performs type checking, scope validation, and other semantic checks.
- **Interpreter**: Executes the parsed AST and prints results.
- **GUI**: Tkinter-based interface for easy interaction and visualization.

## Mini Language Specification

The compiler supports a simple custom language with the following features:

- Variable declarations: `let x = 10;`
- Assignments: `x = x + 5;`
- Arithmetic expressions: `+`, `-`, `*`, `/`
- Print statements: `print(x);`

### Grammar Rules

```
Program     ::= Statement*
Statement   ::= VarDecl | Assign | PrintStmt
VarDecl     ::= 'let' ID '=' Expr ';'
Assign      ::= ID '=' Expr ';'
PrintStmt   ::= 'print' '(' Expr ')' ';'
Expr        ::= Term (( '+' | '-' ) Term)*
Term        ::= Factor (( '*' | '/' ) Factor)*
Factor      ::= ID | NUMBER | '(' Expr ')'
```

### Tokens

- Keywords: `let`, `print`
- Identifiers: `ID` (letters followed by letters/digits/underscores)
- Numbers: `NUMBER` (integers or floats)
- Operators: `+`, `-`, `*`, `/`, `=`
- Punctuation: `(`, `)`, `;`
- EOF: End of file

## Project Structure

```
compiler_project/
├── lexer/
│   ├── tokens.py          # Token definitions
│   └── lexer.py           # Lexical analyzer
├── parser/
│   ├── grammar.md         # Grammar documentation
│   ├── parser.py          # Syntax analyzer and AST
├── semantic/
│   └── semantic_analyzer.py # Semantic analyzer
├── interpreter/
│   └── interpreter.py     # AST interpreter
├── gui/
│   └── main_gui.py        # Tkinter GUI application
├── README.md              # This file
└── requirements.txt       # Dependencies
```

## Installation and Running

1. Ensure Python 3 is installed.
2. No external dependencies are required (Tkinter is built-in).
3. Run the GUI: `python gui/main_gui.py`

## Usage

1. Open the GUI application.
2. Enter your mini-language code in the code editor panel.
3. Click "Lexical Analysis" to see tokens.
4. Click "Syntax Analysis" to view the parse tree.
5. Click "Semantic Analysis" to check for semantic errors.
6. Click "Interpret" to execute the code and see results.

## Example Input

```
let x = 10;
let y = x + 5;
print(y);
```

## Example Output

### Tokens
```
LET 'let' at line 1, col 1
ID 'x' at line 1, col 5
ASSIGN '=' at line 1, col 7
NUMBER '10' at line 1, col 9
SEMI ';' at line 1, col 11
...
```

### Parse Tree
```
Program
├── VarDecl
│   ├── LET 'let'
│   ├── ID 'x'
│   ├── ASSIGN '='
│   ├── Expr
│   │   └── Term
│   │       └── Factor
│   │           └── NUMBER '10'
│   └── SEMI ';'
├── VarDecl
│   ├── LET 'let'
│   ├── ID 'y'
│   ├── ASSIGN '='
│   ├── Expr
│   │   ├── Term
│   │   │   └── Factor
│   │   │       └── ID 'x'
│   │   ├── PLUS '+'
│   │   └── Term
│   │       └── Factor
│   │           └── NUMBER '5'
│   └── SEMI ';'
└── PrintStmt
    ├── PRINT 'print'
    ├── LPAREN '('
    ├── Expr
    │   └── Term
    │       └── Factor
    │           └── ID 'y'
    ├── RPAREN ')'
    └── SEMI ';'
```

### Semantic Analysis
No errors found.

### Interpretation
15

## Screenshots
<img width="1920" height="1080" alt="Screenshot (9)" src="https://github.com/user-attachments/assets/309caee5-e442-455a-88a9-590befcbabb8" />
<img width="1920" height="1080" alt="Screenshot (10)" src="https://github.com/user-attachments/assets/26e3809b-7cfc-451a-adc5-3f44283066e7" />
<img width="1920" height="1080" alt="Screenshot (11)" src="https://github.com/user-attachments/assets/8ad5f938-93f5-4efe-9da1-6a46755f5fa1" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ad851377-0932-4e88-bbbe-8f91ec19e0f0" />


## Contributing

This is an educational project. Feel free to extend it with more language features or optimizations.
