# Python Code Analyzer & Memory Profiler

## Overview
This repository provides a **static code analysis** and **live monitoring** tool for Python projects. It helps identify security issues, code quality problems, performance bottlenecks, and memory inefficiencies.

## Features

### ✅ Static Code Analysis (via `CodeAnalyzer`)
- **Security Issues**
  - Detects hardcoded credentials (passwords, API keys, tokens, etc.).
- **Code Quality Checks**
  - Unused imports and variables detection.
  - Function length and naming convention checks.
- **Performance Issues**
  - Identifies deep recursion and nested loops.
  - Measures cyclomatic complexity and flags high-complexity functions.
- **Readability and Maintainability**
  - Detects missing docstrings.
  - Flags broad exception handling (`except:` without specific exceptions).

### ✅ Runtime Memory Profiling (via `MemoryProfiler`)
- Monitors memory usage (alerts if usage >100 MB).
- Detects large objects (`list`, `dict`, `set` with >10,000 elements).

### ✅ Live Code Monitoring (via `watchdog`)
- Watches for `.py` file modifications.
- Automatically re-analyzes code and updates `analysis_results.json`.

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/python-code-analyzer.git
cd python-code-analyzer

# Install dependencies
pip install -r requirements.txt
```

## Usage
### Run Static Code Analysis
```bash
python code_analyzer.py path/to/your/python/file.py
```

### Run Memory Profiler
```bash
python memory_profiler.py path/to/your/python/file.py
```

### Start Live Monitoring
```bash
python file_watcher.py path/to/your/project/
```

## Output
- Analysis results are saved in `analysis_results.json`.
- Provides suggestions for improving security, performance, and maintainability.

## Contributing
Pull requests are welcome! If you find a bug or have feature suggestions, please open an issue.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

🚀 **Improve your Python code with automated analysis and live monitoring!**

