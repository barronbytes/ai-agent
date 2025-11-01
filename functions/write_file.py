import os


def root_dir() -> str:
    # Returns root path
    file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(file_path)
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    return root_dir


def write_file(directory, file_path, content):
    try:
        full_path = os.path.join(root_dir(), directory, file_path)
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
