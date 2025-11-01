import os

def root_dir() -> str:
    """Returns the root directory of the project."""
    file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(file_path)
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    return root_dir
