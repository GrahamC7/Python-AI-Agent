import sys
import os
from functions.get_files_info import get_files_info

if __name__ == "__main__":
    calc_dir = os.path.abspath("calculator")
    print(get_files_info(calc_dir, "."))
    print(get_files_info(calc_dir, "pkg"))
    print(get_files_info(calc_dir, "/bin"))
    print(get_files_info(calc_dir, "../"))
