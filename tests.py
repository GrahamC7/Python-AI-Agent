import os
import sys
from functions.get_file_content import get_file_content

if __name__ == "__main__":
    calc_dir = os.path.abspath("calculator")
    print(get_file_content(calc_dir, "main.py"))
    print(get_file_content(calc_dir, "pkg/calculator.py"))
    print(get_file_content(calc_dir, "bin/cat"))
