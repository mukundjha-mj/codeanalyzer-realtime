# 🔹 Unused Import Detection
import os  # This import is unused and should be flagged.
import sys  # This import is used below.

# 🔹 Unused Variable Detection
def unused_var_function():
    unused_variable = 10  # Should be flagged as unused.
    print("This function is working!")

# 🔹 Missing Docstring Warning
def missing_docstring_function():
    print("This function has no docstring.")  # Should be flagged.

# 🔹 Cyclomatic Complexity Detection
def complex_function(x):
    if x > 0:
        if x < 10:
            if x % 2 == 0:
                print("Even")  # This function has high complexity.

# 🔹 Deep Recursion Detection
def recurse(n):
    if n == 0:
        return
    recurse(n - 1)  # Should warn if recursion depth is too high.

recurse(10)  # Test recursion depth.

# 🔹 Hardcoded Credentials Warning
password = "mysecretpassword"  # Should be flagged as a security risk.
api_key = "123456789abcdef"  # Hardcoded API key should be flagged.

# 🔹 High Memory Usage Alert
big_list = [i for i in range(10**6)]  # Should warn about high memory usage.

# 🔹 Large Object Detection
big_dict = {i: i for i in range(10000)}  # Should be flagged as a large object.

# 🔹 Inefficient Code Structures Detection (Nested Loops)
for i in range(100):
    for j in range(100):
        for k in range(100):  # This deep nesting should be flagged.
            print(i, j, k)

# 🔹 Used Import
print(sys.version)  # Ensures sys is used and should NOT be flagged.

# 🔹 Function With Proper Docstring
def well_documented_function():
    """This function is correctly documented."""
    print("This should not be flagged.")

# 🔹 Exception Handling (Try-Catch Test)
try:
    1 / 0  # This will cause a division by zero error.
except ZeroDivisionError:
    print("Handled division by zero.")

# 🔹 Open File Without Closing (Resource Leak Detection)
file = open("test.txt", "w")
file.write("This file was opened but not closed!")  # Should detect resource leak.
# Missing file.close() statement!

# 🔹 Multiple Issues in One Function
def bad_function(x):
    """This function has multiple issues."""
    unused_variable = 20  # Unused variable
    if x > 0:
        if x < 10:
            if x % 2 == 0:
                print("Even")  # High complexity
    password = "hardcodedpassword"  # Hardcoded credentials

# Execute functions for testing
unused_var_function()
missing_docstring_function()
complex_function(5)
bad_function(3)

print("✅ All test cases executed. Check your analyzer's output!")
