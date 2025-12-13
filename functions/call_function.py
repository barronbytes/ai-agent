import os
from dotenv import load_dotenv
from google.genai import types
from functions.schemas import *
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


load_dotenv()
WORKING_DIR = os.getenv("WORKING_DIR")
map_to_function = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}
function_schemas = types.Tool(
    # Available functions
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)


def call_function(function_call: types.FunctionCall, verbose: bool=False) -> types.Content:
    '''
    Executes function requested with Gemini model and returns a content object.
    Security check to (1) determine if function exists in available function declarations and
    (2) set "working_directory" argument value for available functions.
    
    Args:
        function_call: Object containing function name and its arguments
        verbose: Optional console argument
    Returns:
        Content object with role set to "tool" and result set to either function call output or error message.
    '''
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f"Calling function: {function_call.name}")

    function_name = function_call.name
    tool_function_content: types.Content | None = None

    # Unsuccessful function call
    if function_name not in map_to_function:
        # Content object created with role "tool" for function call to store default error message
        tool_function_content = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    # Successful function call
    else:
        # Safeguard to set working directory
        args = dict(function_call.args)
        args["working_directory"] = WORKING_DIR

        # Call the actual Python function with unpacked arguments -> function output
        tool_function_output = map_to_function[function_name](**args)

        # Content object created with role "tool" for function call to store actual function call output
        tool_function_content = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": tool_function_output},
                )
            ]
        )

    return tool_function_content
