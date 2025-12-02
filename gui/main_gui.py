import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import tkinter.ttk as ttk
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from lexer.lexer import Lexer
from parser.parser import Parser
from interpreter.interpreter import Interpreter

class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Compiler Front-End Visualizer")
        self.root.geometry("1200x800")

        # Code Editor
        self.code_label = tk.Label(root, text="Source Code:")
        self.code_label.pack(pady=5)
        self.code_editor = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD)
        self.code_editor.pack(fill=tk.X, padx=10, pady=5)
        self.code_editor.insert(tk.END, "let x = 10;\nlet y = x + 5;\nprint(y);")

        self.top_controls = tk.Frame(root)
        self.top_controls.pack(fill=tk.X, padx=10, pady=5)
        self.open_button = tk.Button(self.top_controls, text="Open File", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=5)
        self.save_button = tk.Button(self.top_controls, text="Save Code", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.examples_label = tk.Label(self.top_controls, text="Examples:")
        self.examples_label.pack(side=tk.LEFT, padx=10)
        self.examples_combo = ttk.Combobox(self.top_controls, state="readonly")
        self.examples_combo.pack(side=tk.LEFT, padx=5)
        self.examples_combo.bind("<<ComboboxSelected>>", self.on_example_selected)
        self.load_examples()

        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        self.lex_button = tk.Button(self.button_frame, text="Lexical Analysis", command=self.lexical_analysis)
        self.lex_button.pack(side=tk.LEFT, padx=5)
        self.parse_button = tk.Button(self.button_frame, text="Syntax Analysis", command=self.syntax_analysis)
        self.parse_button.pack(side=tk.LEFT, padx=5)
        self.semantic_button = tk.Button(self.button_frame, text="Semantic Analysis", command=self.semantic_analysis)
        self.semantic_button.pack(side=tk.LEFT, padx=5)
        self.interpret_button = tk.Button(self.button_frame, text="Interpret", command=self.interpret)
        self.interpret_button.pack(side=tk.LEFT, padx=5)
        self.run_all_button = tk.Button(self.button_frame, text="Run All", command=self.run_all)
        self.run_all_button.pack(side=tk.LEFT, padx=5)
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_all_outputs)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.output_frame = tk.Frame(root)
        self.output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.notebook = ttk.Notebook(self.output_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tokens_tab = tk.Frame(self.notebook)
        self.tree_tab = tk.Frame(self.notebook)
        self.semantic_tab = tk.Frame(self.notebook)
        self.console_tab = tk.Frame(self.notebook)

        self.notebook.add(self.tokens_tab, text="Tokens")
        self.notebook.add(self.tree_tab, text="Parse Tree")
        self.notebook.add(self.semantic_tab, text="Semantic")
        self.notebook.add(self.console_tab, text="Console")

        self.tokens_text = scrolledtext.ScrolledText(self.tokens_tab, height=10, wrap=tk.WORD)
        self.tokens_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree_text = scrolledtext.ScrolledText(self.tree_tab, height=18, wrap=tk.WORD)
        self.tree_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.semantic_text = scrolledtext.ScrolledText(self.semantic_tab, height=10, wrap=tk.WORD)
        self.semantic_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.console_text = scrolledtext.ScrolledText(self.console_tab, height=10, wrap=tk.WORD)
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.env_frame = tk.Frame(self.console_tab)
        self.env_frame.pack(fill=tk.X, padx=5, pady=5)
        self.env_label = tk.Label(self.env_frame, text="Environment:")
        self.env_label.pack(anchor=tk.W)
        self.env_tree = ttk.Treeview(self.env_frame, columns=("name", "value"), show="headings", height=6)
        self.env_tree.heading("name", text="Name")
        self.env_tree.heading("value", text="Value")
        self.env_tree.column("name", width=200)
        self.env_tree.column("value", width=200)
        self.env_tree.pack(fill=tk.X)

    def get_code(self):
        return self.code_editor.get("1.0", tk.END).strip()

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.code_editor.delete("1.0", tk.END)
            self.code_editor.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.get_code())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_examples(self):
        examples_path = Path(__file__).resolve().parents[1] / "examples.txt"
        self.examples = []
        titles = []
        try:
            if examples_path.exists():
                with open(examples_path, "r", encoding="utf-8") as f:
                    content = f.read()
                blocks = [b.strip() for b in content.split("---") if b.strip()]
                for b in blocks:
                    lines = b.splitlines()
                    if lines and lines[0].startswith("# Example:"):
                        title = lines[0][10:].strip()
                        code = "\n".join(lines[1:]).strip()
                    else:
                        title = f"Example {len(self.examples) + 1}"
                        code = b
                    self.examples.append((title, code))
                    titles.append(title)
        except Exception:
            pass
        self.examples_combo["values"] = titles
        if titles:
            self.examples_combo.current(0)

    def on_example_selected(self, event=None):
        idx = self.examples_combo.current()
        if idx is None or idx < 0:
            return
        title, code = self.examples[idx]
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert(tk.END, code)

    def lexical_analysis(self):
        code = self.get_code()
        lexer = Lexer(code)
        tokens, errors = lexer.tokenize()
        self.tokens_text.delete("1.0", tk.END)
        if errors:
            self.tokens_text.insert(tk.END, "Errors:\n" + "\n".join(errors))
        else:
            for token in tokens:
                self.tokens_text.insert(tk.END, f"{token.type.name} '{token.lexeme}' at line {token.line}, col {token.column}\n")
        self.notebook.select(self.tokens_tab)

    def syntax_analysis(self):
        code = self.get_code()
        lexer = Lexer(code)
        tokens, lex_errors = lexer.tokenize()
        if lex_errors:
            self.tree_text.delete("1.0", tk.END)
            self.tree_text.insert(tk.END, "Lexical errors found. Fix them first.\n" + "\n".join(lex_errors))
            return
        parser = Parser(tokens)
        ast, parse_errors = parser.parse()
        self.tree_text.delete("1.0", tk.END)
        if parse_errors:
            self.tree_text.insert(tk.END, "Parse errors:\n" + "\n".join(parse_errors))
        else:
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            parser.print_tree(ast)
            sys.stdout = old_stdout
            self.tree_text.insert(tk.END, buffer.getvalue())
        self.notebook.select(self.tree_tab)

    def semantic_analysis(self):
        code = self.get_code()
        lexer = Lexer(code)
        tokens, lex_errors = lexer.tokenize()
        if lex_errors:
            self.semantic_text.delete("1.0", tk.END)
            self.semantic_text.insert(tk.END, "Lexical errors found. Fix them first.\n" + "\n".join(lex_errors))
            return
        parser = Parser(tokens)
        ast, parse_errors = parser.parse()
        if parse_errors:
            self.semantic_text.delete("1.0", tk.END)
            self.semantic_text.insert(tk.END, "Parse errors found. Fix them first.\n" + "\n".join(parse_errors))
            return
        try:
            from semantic.semantic_analyzer import SemanticAnalyzer
            analyzer = SemanticAnalyzer()
        except Exception as e:
            self.semantic_text.delete("1.0", tk.END)
            self.semantic_text.insert(tk.END, f"Semantic analyzer unavailable: {e}")
            return
        errors = analyzer.analyze(ast)
        self.semantic_text.delete("1.0", tk.END)
        if errors:
            self.semantic_text.insert(tk.END, "\n".join(errors))
        else:
            self.semantic_text.insert(tk.END, "No semantic errors found.")
        self.notebook.select(self.semantic_tab)

    def interpret(self):
        code = self.get_code()
        lexer = Lexer(code)
        tokens, lex_errors = lexer.tokenize()
        if lex_errors:
            self.interpret_text.delete("1.0", tk.END)
            self.interpret_text.insert(tk.END, "Lexical errors found. Fix them first.\n" + "\n".join(lex_errors))
            return
        parser = Parser(tokens)
        ast, parse_errors = parser.parse()
        if parse_errors:
            self.console_text.delete("1.0", tk.END)
            self.console_text.insert(tk.END, "Parse errors found. Fix them first.\n" + "\n".join(parse_errors))
            return
        try:
            from semantic.semantic_analyzer import SemanticAnalyzer
            analyzer = SemanticAnalyzer()
        except Exception as e:
            self.interpret_text.delete("1.0", tk.END)
            self.interpret_text.insert(tk.END, f"Semantic analyzer unavailable: {e}")
            return
        sem_errors = analyzer.analyze(ast)
        if sem_errors:
            self.console_text.delete("1.0", tk.END)
            self.console_text.insert(tk.END, "Semantic errors found. Fix them first.\n" + "\n".join(sem_errors))
            return
        interpreter = Interpreter(ast)
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        result = interpreter.interpret()
        output = buffer.getvalue()
        sys.stdout = old_stdout
        self.console_text.delete("1.0", tk.END)
        self.console_text.insert(tk.END, output + "\n" + result)
        for i in self.env_tree.get_children():
            self.env_tree.delete(i)
        for k, v in interpreter.environment.items():
            self.env_tree.insert("", tk.END, values=(k, v))
        self.notebook.select(self.console_tab)

    def clear_other_outputs(self):
        self.semantic_text.delete("1.0", tk.END)
        self.console_text.delete("1.0", tk.END)

    def clear_all_outputs(self):
        self.tokens_text.delete("1.0", tk.END)
        self.tree_text.delete("1.0", tk.END)
        self.semantic_text.delete("1.0", tk.END)
        self.console_text.delete("1.0", tk.END)
        for i in self.env_tree.get_children():
            self.env_tree.delete(i)

    def run_all(self):
        self.lexical_analysis()
        self.syntax_analysis()
        self.semantic_analysis()
        self.interpret()

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()
