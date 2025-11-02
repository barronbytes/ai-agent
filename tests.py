import os
from functions.run_python_file import run_python_file


def test():
    directory= "calculator"
    t1 = run_python_file(directory, "main.py")
    t2 = run_python_file(directory, "main.py", ["3 + 5"])
    t3 = run_python_file(directory, "tests.py")
    t4 = run_python_file(directory, "../main.py")
    t5 = run_python_file(directory, "nonexistent.py")
    t6 = run_python_file(directory, "lorem.txt")
    print(t1)
    print(t2)
    print(t3)
    print(t4)
    print(t5)
    print(t6)


if __name__ == "__main__":
    test()
