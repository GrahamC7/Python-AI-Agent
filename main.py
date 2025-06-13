import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# system prompt for the LLM
system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

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
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)

# Print the response text
print(response.text)

# Print token usage details
if args.verbose:
    print(f"User prompt: {args.prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")