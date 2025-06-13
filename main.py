import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


function_map = {
    "get_files_info": lambda **kwargs: __import__('functions.get_files_info', fromlist=['get_files_info']).get_files_info(**kwargs),
    "get_file_content": lambda **kwargs: __import__('functions.get_file_content', fromlist=['get_file_content']).get_file_content(**kwargs),
    "run_python_file": lambda **kwargs: __import__('functions.run_python', fromlist=['run_python_file']).run_python_file(**kwargs),
    "write_file": lambda **kwargs: __import__('functions.write_file', fromlist=['write_file']).write_file(**kwargs),
}


def call_function(function_call_part, verbose=False):
    """
    Calls the specified function with the provided arguments.
    Prints the function name and arguments if verbose is True,
    otherwise just prints the function name.
    """
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    # prepare arguments and add working directory
    kwargs = dict(function_call_part.args)
    kwargs['working_directory'] = "./calculator"  # set the working directory
    func = function_map.get(function_call_part.name)
    if func:
        result = func(**kwargs)
        print(f"Result: {result}")
        return result
    else:
        print(f"Error: Function {function_call_part.name} not found.")
        return types.Content(
            role="tool",
            parts=[
                type.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )


# system prompt for the LLM
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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


# function declaration scheme for get_file_content
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of the specified file as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
        },
    ),
)


# function declaration scheme for run_python_file
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and returns its output, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)


# function declaration scheme for write_file
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file at the specified path, creating it if it doesn't exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)


# list of available functions (tools)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
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


if hasattr(response, 'function_calls') and response.function_calls:
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=args.verbose)
        # Handle result type
        if isinstance(function_call_result, str):
            if args.verbose:
                print(f"-> {function_call_result}")
        elif hasattr(function_call_result, "parts") and function_call_result.parts:
            try:
                response_data = function_call_result.parts[0].function_response.response
                if args.verbose:
                    print(f"-> {response_data}")
            except (AttributeError, IndexError):
                raise RuntimeError("Fatal: Function did not return a valid types.Content with a function_response.response.")
        else:
            raise RuntimeError("Fatal: Function did not return a valid result.")
else:
    print(response.text)


# Print token usage details
if args.verbose:
    print(f"User prompt: {args.prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")