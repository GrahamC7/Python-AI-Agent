import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        if os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
        else:
            file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # ensure the file is within the working directory
        if not os.path.commonpath([working_directory, file_path]) == working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted directory'
        
        # if file_path does not exist, return an error
        if not os.path.exists(file_path):
            return f'Error: File "{file_path}" not found'
        
        # if file does not end with .py, return an error
        if not file_path.endswith('.py'):
            return f'Error: File "{file_path}" is not a Python file'
        
        # use subprocess to run the Python file
        try:
            result = subprocess.run(
                ['python', file_path],
                cwd=working_directory, # set working directory
                capture_output=True, # capture both stdout and stderr
                text=True
                timeout=30 # set timeout to 30 seconds to prevent infinite execution
            )
        except subprocess.TimeoutExpired:
            return f'Error: Execution of "{file_path}" timed out after 30 seconds'
        
        output_lines = []
        if result.stdout.strip(): # stdout
            output_lines.append(f'Output:\n{result.stdout.strip()}')
        if result.stderr.strip(): #stderr
            output_lines.append(f'Error:\n{result.stderr.strip()}')
        if result.returncode != 0: # non-zero exit code
            output_lines.append(f'Error: Script "{file_path}" exited with code X')
        if not output_lines: # no output produced error
            return "No output produced."
        return '\n'.join(output_lines)
    except Exception as e:
        return f'Error: executiing Python file: {e}'
