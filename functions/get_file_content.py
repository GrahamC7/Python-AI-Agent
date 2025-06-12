import os

def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        if os.path.isabs(file_path):
            abs_file_path = os.path.abspath(file_path)
        else:
            abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # ensure the file is within the working directory
        if not os.path.commonpath([working_directory, abs_file_path]) == working_directory:
            return f'Error: Cannot access "{abs_file_path}" as it is outside the permitted directory'
        
        # ensure the path is a file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f'Error: {str(e)}'