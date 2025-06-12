import os
from functions.write_file import write_file
from functions.run_python import run_python_file

if __name__ == "__main__":
    calc_dir = os.path.abspath("calculator")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))  # should not be allowed
    print(run_python_file("calculator", "nonexistent.py"))  # should not be allowed
