import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


if len(sys.argv) == 1:
    print("Error: No prompt argument provided.")
    print("Usage: python main.py 'your prompt here'")
    print("Example: python main.py 'How do I build a calculator app?'")
    sys.exit(1)


def generate_response(client, messages):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
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
    load_dotenv()
    args = sys.argv[1:]
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(args)
    is_verbose = bool(args[-1] == "--verbose")
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = generate_response(client, messages)
    generate_content(response, user_prompt, is_verbose)


if __name__ == "__main__":
    main()
