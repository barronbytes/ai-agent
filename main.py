import sys # interact with Python runtime → interpreter settings, arguments, system-level information
import os # interact with operating system → files, directories, environmental variables, processes
from dotenv import load_dotenv  # type: ignore
from google import genai
from google.genai import types  # type: ignore


load_dotenv()
AI_MODEL = "gemini-2.0-flash-001"


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


def generate_response(client, messages):
    system_prompt=os.getenv("SYSTEM_PROMPT")
    response = client.models.generate_content(
        model=AI_MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
        ),
    )
    return response


def generate_content(response, user_prompt, is_verbose):
    if is_verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)


def main():
    user_prompt, is_verbose = get_system_prompts()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = generate_response(client, messages)
    generate_content(response, user_prompt, is_verbose)


if __name__ == "__main__":
    main()
