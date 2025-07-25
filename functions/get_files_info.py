import os


def root_dir() -> str:
    # Returns root path
    file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(file_path)
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    return root_dir


def get_contents(working_directory, directory):
    # Returns directory contents if path originals from root path, otherwise returns error message
    try:
        full_path = os.path.join(working_directory, directory)
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)): # valid path but not from root directory
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path): # valid path but not a directory (i.e., a file)
            return f'Error: "{directory}" is not a valid directory'
        return os.listdir(full_path)
    except Exception as e:
        return f"Error: {str(e)}" # invalid path provided, etc.


def get_files_info(working_directory, directory="."):
    contents = get_contents(working_directory, directory)
    if isinstance(contents, str) and contents.startswith("Error:"):
        return contents

    lines = []
    for item in contents:
        try:
            item_path = os.path.join(working_directory, directory, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        except Exception as e:
            lines.append(f"- {item}: Error: {str(e)}")
    return lines

print(get_files_info(root_dir(), "."))
