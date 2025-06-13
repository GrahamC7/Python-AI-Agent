import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


# system prompt for the LLM
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


# function declaration scheme for get_files_info
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


# list of available functions (tools)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ],
)


# Load the API key from .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Ask Gemini a question and get a response.")
parser.add_argument("prompt", type=str, nargs='?', help="Prompt to send to Gemini")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


# Custom error if prompt is not provided
if not args.prompt:
    print("Error: No prompt provided. Please provide a prompt as an argument.")
    print("Usage: python3 main.py <prompt>")
    sys.exit(1)


# Create a Gemini client
client = genai.Client(api_key=api_key)


# Generate a response using the specified model and prompt
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=args.prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions],
    ),
)


# Check if the response contains function calls
if hasattr(response, 'function_calls') and response.function_calls:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({repr(function_call.args)})")
else:
    print(response.text)


# Print token usage details
if args.verbose:
    print(f"User prompt: {args.prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")