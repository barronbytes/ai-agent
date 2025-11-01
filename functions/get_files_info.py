import os


def root_dir() -> str:
    # Returns root path
    file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(file_path)
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    return root_dir


def get_contents(working_directory, directory):
    # Returns the contents of a directory if it is within the root path; otherwise, returns an error message
    try:
        full_path = os.path.join(working_directory, directory)
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            # valid path but not from root directory
            # safeguards against `traversal attacks` like `directory=..\..\..`
        if not os.path.isdir(full_path): # valid path but not a directory (i.e., a file)
            return f'Error: "{directory}" is not a valid directory'
        return os.listdir(full_path)
    except Exception as e:
        return f"Error: {str(e)}" # invalid path provided, etc.


def get_files_info(working_directory, directory="."):
    contents = get_contents(working_directory, directory)
    if isinstance(contents, str) and contents.startswith("Error:"):
        return (contents, directory)

    lines = []
    for item in contents:
        try:
            item_path = os.path.join(working_directory, directory, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        except Exception as e:
            lines.append(f"- {item}: Error: {str(e)}")
    return (lines, directory)


def generate_report(lines, directory):
    message = ""
    if isinstance(lines, str) and lines.startswith("Error:"):                                        
        message = '\tError: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        message = "\n".join(lines)
    return f"Result for '{directory}' directory:\n{message}"

lines, directory = get_files_info(root_dir(), "calculator/pkg")
message = generate_report(lines, directory)
print(message)
