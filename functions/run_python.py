import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        original_file_path = file_path  # Save for error messages
        working_directory = os.path.abspath(working_directory)
        if os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
        else:
            file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # ensure the file is within the working directory
        if not os.path.commonpath([working_directory, file_path]) == working_directory:
            return f'Error: Cannot execute "{original_file_path}" as it is outside the permitted directory'
        
        # if file_path does not exist, return an error
        if not os.path.exists(file_path):
            return f'Error: File "{os.path.basename(file_path)}" not found'
        
        # if file does not end with .py, return an error
        if not file_path.endswith('.py'):
            return f'Error: File "{original_file_path}" is not a Python file'
        
        try:
            result = subprocess.run(
                ['python', file_path],
                cwd=working_directory,
                capture_output=True,
                text=True,
                timeout=30
            )
        except subprocess.TimeoutExpired:
            return f'Error: Execution of "{original_file_path}" timed out after 30 seconds'
        
        output_lines = []
        if result.stdout.strip():
            output_lines.append(f'Output:\n{result.stdout.strip()}')
        if result.stderr.strip():
            output_lines.append(f'Error:\n{result.stderr.strip()}')
        if result.returncode != 0:
            output_lines.append(f'Error: Script "{original_file_path}" exited with code X')
        if not output_lines:
            return "No output produced."
        return '\n'.join(output_lines)
    except Exception as e:
        return f'Error: executiing Python file: {e}'