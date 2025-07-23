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


def generate_content(client, messages):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
    )
    return response


def response_output(response, user_prompt, final_prompt):
    if final_prompt == "--verbose":
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
    final_prompt = args[-1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = generate_content(client, messages)
    response_output(response, user_prompt, final_prompt)


if __name__ == "__main__":
    main()
