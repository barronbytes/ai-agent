import os
from functions.utils import root_dir


def write_file(working_directory: str, file_path: str, content: str) -> str:
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
