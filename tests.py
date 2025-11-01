import os
#from functions.get_files_info import get_files_info, generate_report, root_dir
from functions.get_file_content import get_file_content

def test():
    directory= "calculator"
    
    print(get_file_content(directory, "main.py"))
    print()
    print(get_file_content(directory, "pkg/calculator.py"))
    print()
    print(get_file_content(directory, "/bin/cat"))
    print()
    print(get_file_content(directory, "pkg/does_not_exist.py"))


"""
def test():
    working_dir = root_dir()

    # Test current directory
    print(generate_report(*get_files_info(working_dir, ".")))
    print()

    # Test calculator/pkg directory
    calc_dir = os.path.join(working_dir, "calculator")
    print(generate_report(*get_files_info(calc_dir, "pkg")))
    print()

    # Test invalid /bin directory
    print(generate_report(*get_files_info(working_dir, "/bin")))
    print()

    # Test invalid ../ directory
    print(generate_report(*get_files_info(working_dir, "../")))
"""


if __name__ == "__main__":
    test()
