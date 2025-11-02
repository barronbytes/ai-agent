import sys # interact with Python runtime → interpreter settings, arguments, system-level information
import os # interact with operating system → files, directories, environmental variables, processes
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")


if len(sys.argv) == 1:
    print("Error: No prompt argument provided.")
    print("Usage: python main.py 'your prompt here'")
    print("Example: python main.py 'How do I build a calculator app?'")
    sys.exit(1)


def get_system_prompts():
    args = sys.argv[1:] # index 0 is always the Python file name, so it can be ignored
    user_prompt = " ".join(args)
    is_verbose = bool(args[-1] == "--verbose")
    return [user_prompt, is_verbose]


def get_response(client, config, contents):
    return client.models.generate_content(
        model=AI_MODEL,
        config=config,
        contents=contents,
    )


def print_report(response, user_prompt, is_verbose):
    if is_verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    
    if not response.function_calls:
        print("Response:")
        print(response.text)
    else:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")


def main():
    # Step #1: Define a function declaration (done in functions.get_files_info)
    # Step #2: Call the model with function declarations

    # Configure the client and tools
    client = genai.Client(api_key=API_KEY)
    tools = types.Tool(
        # Available functions
        function_declarations=[
            schema_get_files_info,
        ]
    )
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
    print_report(response, user_prompt, is_verbose)


if __name__ == "__main__":
    main()
