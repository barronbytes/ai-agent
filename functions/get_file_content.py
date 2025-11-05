import os
from dotenv import load_dotenv
from functions.utils import root_dir


load_dotenv()
MAX_CHAR_LIMIT = int(os.getenv("MAX_CHAR_LIMIT"))


def get_file_content(working_directory: str, file_path: str) -> str:
    # Returns the contents of a file if it is within the root path; otherwise, returns an error message
    try:
        full_path = os.path.join(root_dir(), working_directory, file_path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(root_dir())):
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
            # valid path but not from root directory
            # safeguards against `traversal attacks` like `file_path=..\..\..`
        if not os.path.isfile(full_path): # valid path but not a file (i.e., a directory)
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_path, mode="r", encoding="utf-8") as f:
            content = f.read()
            return content[:MAX_CHAR_LIMIT]  # truncate to limit
    except Exception as e:
        return f"Error: {str(e)}" # invalid file path provided, etc.    
