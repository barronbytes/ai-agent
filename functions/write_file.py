import os
from functions.utils import root_dir


def write_file(working_directory: str, file_path: str, content: str) -> str:
    '''
    Writes content to a file relative to a working directory, automatically creating parent directories
    if neccessary and overwritting files if already present. A security check is enforced to prevent
    directory traversal outside the permitted root directory.

    Args:
        working_directory: The base directory where the file is located.
        file_path: The path to the Python file, relative to the working directory.
        content: The string content to be written to the file.
    Returns:
        Output string for success or error message.
    '''
    try:
        full_path = os.path.join(root_dir(), working_directory, file_path)
        # Safeguard against directory traversal
        if not os.path.abspath(full_path).startswith(os.path.abspath(root_dir())):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure parent directories exists, create file, and overwrite
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}": ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}" # invalid file path provided, etc.    
