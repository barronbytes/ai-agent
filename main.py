import sys # interact with Python runtime → interpreter settings, arguments, system-level information
import os # interact with operating system → files, directories, environmental variables, processes
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.schemas import *
from functions.call_function import function_schemas, call_function


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")


if len(sys.argv) == 1:
    print("Error: No prompt argument provided.")
    print("Usage: python main.py 'your prompt here'")
    print("Example: python main.py 'How do I build a calculator app?'")
    sys.exit(1)


def get_system_prompts() -> tuple[str, bool]:
    args = sys.argv[1:] # index 0 is always the Python file name, so it can be ignored
    user_prompt = " ".join(args)
    is_verbose = bool(args[-1] == "--verbose")
    return (user_prompt, is_verbose)


def get_response(
    client: genai.Client, 
    config: types.GenerateContentConfig, 
    contents: list[types.Content]
) -> types.GenerateContentResponse:
    return client.models.generate_content(
        model=AI_MODEL,
        config=config,
        contents=contents,
    )


def get_function_response_parts(
    response: types.GenerateContentResponse, 
    user_prompt: str, 
    is_verbose: bool
) -> list[types.Part]:
    if is_verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_response_parts: list[types.Part] = []
    if not response.function_calls:
        print("Response:")
        print(response.text)
    else:
        # Function execution
        for function_call in response.function_calls:
            tool_function_content = call_function(function_call, is_verbose)
        
            if not tool_function_content.parts or not tool_function_content.parts[0].function_response:
                raise Exception("Empty function call result")

            if is_verbose:
                print(f"-> {tool_function_content.parts[0].function_response.response}")

            # Function execution results
            function_response_parts.append(tool_function_content.parts[0])
        if not function_response_parts:
            raise Exception("No function responses generated, exiting.")

    return function_response_parts


def main():
    # Step #1: Define a function declaration (done in functions.<file_names>.py)
    # Step #2: Call the model with function declarations

    # Configure the client and tools
    client = genai.Client(api_key=API_KEY)
    tools = function_schemas
    config=types.GenerateContentConfig(
        tools=[tools], system_instruction=SYSTEM_PROMPT
    )

    # Define user prompt
    user_prompt, is_verbose = get_system_prompts()
    contents = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Send request with function declarations
    response = get_response(client, config, contents)

    # Step 3: Execute the functions requested by the model and collect responses
    get_function_response_parts(response, user_prompt, is_verbose)


if __name__ == "__main__":
    main()
