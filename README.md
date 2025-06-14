# Python AI Agent

This project is an **AI-powered coding agent** that uses Google Gemini to analyze, reason about, and modify Python code in a workspace. The agent can list files, read file contents, write or overwrite files, and execute Python scripts—all through natural language prompts.

## Features

- **Conversational Agent:** Maintains a conversation history and iteratively interacts with the LLM to solve tasks.
- **Function Calling:** The agent can call specific Python functions (tools) to interact with the filesystem and codebase.
- **Feedback Loop:** The agent can use the results of its own actions to plan further steps, enabling multi-step problem solving.
- **Extensible:** Easily add new tools/functions for the agent to use.

## Supported Operations

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

## Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd python-ai-agent
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up your Gemini API key:**
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_google_gemini_api_key_here
     ```

## Usage

Run the agent with a natural language prompt:

```sh
python3 main.py "fix the bug: 3 + 7 * 2 shouldn't be 20"
```

You can also use the `--verbose` flag to see detailed output:

```sh
python3 main.py --verbose "list the contents of the pkg directory"
```

## Example Prompts

- `list the contents of the pkg directory`
- `read the contents of main.py`
- `write 'hello world' to hello.txt`
- `run main.py`
- `fix the bug: 3 + 7 * 2 shouldn't be 20`

## How It Works

1. **Prompt:** You provide a natural language instruction.
2. **Agent Loop:** The agent sends the conversation history to Gemini, which may respond with a plan or a function call.
3. **Function Execution:** If a function call is requested, the agent executes it and appends the result to the conversation.
4. **Iteration:** The agent continues this loop, using the results of previous steps, until the task is complete.

## Adding New Tools

To add a new function/tool:
1. Implement the function in the `functions/` directory.
2. Add a function declaration schema in `main.py`.
3. Add the function to the `function_map` and `available_functions`.

## License

MIT License

---

**Note:** This project is for educational and experimental purposes. Use with caution on important files or codebases.
