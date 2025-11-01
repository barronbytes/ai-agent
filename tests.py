import os
from functions.write_file import write_file


def test():
    directory= "calculator"
    t1 = write_file(directory, "lorem.txt", "wait, this isn't lorem ipsum")
    t2 = write_file(directory, "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    t3 = write_file(directory, "/tmp/temp.txt", "this should not be allowed")
    print(t1, "\n")
    print(t2, "\n")
    print(t3, "\n")


if __name__ == "__main__":
    test()
