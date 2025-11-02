import os
from functions.utils import root_dir
from google.genai import types


def get_files_info(working_directory, directory="."):
    """
    Returns files with metadata at the path: root_dir() + working_directory + directory
    """
    contents = []
    try:
        full_path = os.path.join(root_dir(), working_directory, directory)
        # safeguard against directory traversal (e.g., directory=..\..\..)
        if not os.path.abspath(full_path).startswith(os.path.abspath(root_dir())):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a valid directory'

        contents = os.listdir(full_path)
    except Exception as e:
        return f"Error: {str(e)}"

    try:
        files_info = []
        for item in contents:
            item_path = os.path.join(full_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            files_info.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)
    except Exception as e:
            return f"- Error: Cannot list file: {str(e)}"


# Step #1: Define a function declaration
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)