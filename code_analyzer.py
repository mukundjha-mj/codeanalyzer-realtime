import ast
import os
import re
import psutil
import time
import json
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.issues = []
        self.function_complexity = {}
        self.memory_warnings = []
        self.unused_imports = set()
        self.imports = set()
        self.defined_variables = set()
        self.used_variables = set()
        self.function_lengths = {}
        self.lines = {}

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.lines[node.lineno] = node
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
        self.lines[node.lineno] = node
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Detect hardcoded credentials
        for target in node.targets:
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Str):
                if re.search(r'(password|key|token|secret)', target.id, re.IGNORECASE):
                    self.issues.append(f"[SECURITY] Line {node.lineno}: Hardcoded credential found: {target.id}")
        self.lines[node.lineno] = node
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if not ast.get_docstring(node):
            self.issues.append(f"[READABILITY] Line {node.lineno}: Function '{node.name}' is missing a docstring.")
        
        # Detect recursion
        recursion_count = sum(1 for n in ast.walk(node) if isinstance(n, ast.Call) and getattr(n.func, 'id', None) == node.name)
        if recursion_count > 3:
            self.issues.append(f"[PERFORMANCE] Line {node.lineno}: Deep recursion detected in function '{node.name}'.")

        function_length = len(node.body)
        if function_length > 50:
            self.issues.append(f"[CODE QUALITY] Line {node.lineno}: Function '{node.name}' is too long ({function_length} lines).")
        self.function_lengths[node.name] = function_length

        if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
            self.issues.append(f"[STYLE] Line {node.lineno}: Function '{node.name}' does not follow snake_case naming.")

        complexity = sum(isinstance(n, (ast.If, ast.For, ast.While, ast.Try, ast.With)) for n in ast.walk(node))
        self.function_complexity[node.name] = complexity
        if complexity > 10:
            self.issues.append(f"[COMPLEXITY] Line {node.lineno}: High cyclomatic complexity ({complexity}) in function '{node.name}'.")

        self.lines[node.lineno] = node
        self.generic_visit(node)

    def visit_For(self, node):
        nested_loops = sum(isinstance(n, (ast.For, ast.While)) for n in ast.walk(node))
        if nested_loops > 2:
            self.issues.append(f"[PERFORMANCE] Line {node.lineno}: Deeply nested loops detected, consider refactoring.")
        self.lines[node.lineno] = node
        self.generic_visit(node)

    def visit_While(self, node):
        nested_loops = sum(isinstance(n, (ast.For, ast.While)) for n in ast.walk(node))
        if nested_loops > 2:
            self.issues.append(f"[PERFORMANCE] Line {node.lineno}: Deeply nested loops detected, consider refactoring.")
        self.lines[node.lineno] = node
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined_variables.add(node.id)
        else:
            self.used_variables.add(node.id)
        self.lines[node.lineno] = node
        self.generic_visit(node)

    def analyze(self):
        self.unused_imports = self.imports - self.used_variables
        suggestions = []

        for imp in self.unused_imports:
            issue = f"[CODE QUALITY] Unused import detected: {imp}"
            self.issues.append(issue)
            suggestions.append({"issue": issue, "suggestion": f"Remove the unused import '{imp}'."})

        unused_vars = self.defined_variables - self.used_variables
        for var in unused_vars:
            issue = f"[CODE QUALITY] Unused variable detected: {var}"
            self.issues.append(issue)
            suggestions.append({"issue": issue, "suggestion": f"Remove or use the unused variable '{var}' to improve efficiency."})

        for issue in self.issues:
            # Hardcoded credentials
            if "[SECURITY] Hardcoded credential found:" in issue:
                var_name = issue.split(":")[-1].strip()
                suggestions.append({"issue": issue, "suggestion": f"Store '{var_name}' in an environment variable instead of hardcoding it."})

            # Missing docstrings
            if "[READABILITY] Function" in issue and "is missing a docstring" in issue:
                func_name = issue.split("'")[1]
                suggestions.append({"issue": issue, "suggestion": f"Add a docstring to the function '{func_name}' to improve readability."})

            # Deep recursion
            if "[PERFORMANCE] Deep recursion detected" in issue:
                func_name = issue.split("'")[1]
                suggestions.append({"issue": issue, "suggestion": f"Consider using iteration or memoization to optimize function '{func_name}'."})

            # Long functions
            if "[CODE QUALITY] Function" in issue and "is too long" in issue:
                func_name = issue.split("'")[1]
                suggestions.append({"issue": issue, "suggestion": f"Break '{func_name}' into smaller functions for better readability and maintainability."})

            # High cyclomatic complexity
            if "[COMPLEXITY] High cyclomatic complexity" in issue:
                func_name = issue.split("'")[1]
                suggestions.append({"issue": issue, "suggestion": f"Refactor '{func_name}' to reduce complexity by splitting logic into smaller functions."})

            # Deeply nested loops
            if "[PERFORMANCE] Deeply nested loops detected" in issue:
                suggestions.append({"issue": issue, "suggestion": "Refactor nested loops by breaking them into separate functions or using list comprehensions."})

        # Exception handling improvement
        with open(self.filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if "except:" in line and "Exception" not in line:
                    issue = f"[ERROR HANDLING] Line {i+1}: Catching a broad exception (except:)."
                    self.issues.append(issue)
                    suggestions.append({"issue": issue, "suggestion": "Use 'except Exception as e:' to avoid catching all errors blindly."})

        return {
            "filename": self.filename,
            "issues": self.issues,
            "function_complexity": self.function_complexity,
            "function_lengths": self.function_lengths,
            "unused_imports": list(self.unused_imports),
            "suggestions": suggestions
        }



class MemoryProfiler:
    @staticmethod
    def get_memory_usage():
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)

    @staticmethod
    def check_large_objects():
        large_objects = []
        for name, obj in globals().items():
            if isinstance(obj, (list, dict, set)) and len(obj) > 10000:
                large_objects.append(name)
        return large_objects

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.file_hashes = {}

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            with open(event.src_path, 'rb') as f:
                new_hash = hashlib.md5(f.read()).hexdigest()
            if event.src_path in self.file_hashes and self.file_hashes[event.src_path] == new_hash:
                return
            self.file_hashes[event.src_path] = new_hash

            print(f"\n🔄 File '{event.src_path}' changed, re-analyzing...")
            results = analyze_file(event.src_path)
            with open("analysis_results.json", "w") as outfile:
                json.dump(results, outfile, indent=4)
            print(f"📄 Analysis updated: {json.dumps(results, indent=4)}")

def analyze_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    tree = ast.parse(code)
    analyzer = CodeAnalyzer(filepath)
    analyzer.visit(tree)
    results = analyzer.analyze()

    memory_usage = MemoryProfiler.get_memory_usage()
    if memory_usage > 100:
        results["issues"].append(f"[PERFORMANCE] High memory usage: {memory_usage:.2f} MB")

    large_objects = MemoryProfiler.check_large_objects()
    if large_objects:
        results["issues"].append(f"[PERFORMANCE] Large objects detected: {large_objects}")

    with open("analysis_results.json", "w") as outfile:
        json.dump(results, outfile, indent=4)

    return results

def monitor_directory(directory):
    event_handler = FileChangeHandler(CodeAnalyzer)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    print(f"📡 Live Monitoring Started in '{directory}'... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_directory(os.getcwd())


