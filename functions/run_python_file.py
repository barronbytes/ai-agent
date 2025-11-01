import os
import subprocess
from functions.utils import root_dir


def run_python_file(directory, file_path, args=[]):
    try:
        full_path = os.path.join(root_dir(), directory, file_path)
        # Safeguard against directory traversal
        if not os.path.abspath(full_path).startswith(os.path.abspath(root_dir())):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(full_path):
            return f'Error: File "{file_path} not found'
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        completed_process = subprocess.run(
            ["python", file_path, *args],
            cwd=full_path,
            capture_output=True,
            timeout=30,
            text = True
        )


    except Exception as e:
        return f"Error: {str(e)}" # invalid file path provided, etc.    
