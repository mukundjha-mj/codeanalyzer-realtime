import os
import json
import hashlib

password = "123456"

def MissingDocstringFunction(x, y):
    return x + y

def deep_recursion(n):
    if n <= 0:
        return 1
    return n * deep_recursion(n - 1)

def long_function():
    for i in range(10):
        for j in range(10):
            for k in range(10):
                print(i, j, k)

def complex_function(x):
    if x > 0:
        if x < 10:
            while x > 0:
                x -= 1
        elif x < 20:
            for i in range(x):
                if i % 2 == 0:
                    x -= 1
                else:
                    x += 1
        else:
            try:
                x = int("invalid")
            except:
                x = 0
    return x

def unused_function():
    x = 10

def except_without_exception():
    try:
        x = 1 / 0
    except:
        x = 0
    return x

def large_memory_usage():
    big_list = [i for i in range(20000)]
    big_dict = {i: i for i in range(20000)}
    return big_list, big_dict

x = 5
y = 10
z = x + y
