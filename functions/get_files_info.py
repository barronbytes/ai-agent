import os
from functions.utils import root_dir


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
