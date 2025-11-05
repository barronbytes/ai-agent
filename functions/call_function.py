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
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f"Calling function: {function_call.name}")

    function_name = function_call.name
    tool_function_content: types.Content | None = None

    # Unsuccessful function call
    if function_name not in map_to_function:
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
        # Security measure to set working directory
        args = dict(function_call.args)
        args["working_directory"] = WORKING_DIR
        tool_function = map_to_function[function_name](**args)
        tool_function_content = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": tool_function},
                )
            ]
        )

    return tool_function_content
