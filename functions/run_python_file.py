import os
import subprocess
from functions.utils import root_dir


def run_python_file(working_directory: str, file_path: str, args: list[str]=[]) -> str:
    '''
    Runs a specified Python file within the working directory with optional arguments.
    A security check is enforced to prevent directory traversal outside the permitted root directory.

    Args:
        working_directory: The base directory where the file is located.
        file_path: The path to the Python file, relative to the working directory.
        args: Optional list of string arguments to pass to the script.
    Returns:
        Output string (STDOUT, STDERR, and return code) of the executed script.
    '''
    try:
        full_path = os.path.join(root_dir(), working_directory, file_path)
        # Safeguard against directory traversal
        if ".." in file_path.split(os.path.sep) or not os.path.abspath(full_path).startswith(os.path.abspath(root_dir())):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found'
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        # Executes a Python file
        # ["python", file_path, *args] forms the command: python <file_path> <arg1> <arg2>...
        completed_process = subprocess.run(
            ["python", file_path, *args],
            cwd=os.path.dirname(full_path),
            capture_output=True, # Captures STDOUT and STDERR
            timeout=30, # Safeguard to limit time
            text = True
        )

        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()
        return_code = completed_process.returncode

        output_parts = []
        if stdout:
            output_parts.append(f'STDOUT: {stdout}')
        if stderr:
            output_parts.append(f'STDERR: {stderr}')
        if return_code != 0:
            output_parts.append(f'Process exited with code {return_code}')

        final_output = "\n".join(output_parts) if output_parts else "No output produced"
        return final_output

    except Exception as e:
        return f"Error: executing Python file: {str(e)}"
