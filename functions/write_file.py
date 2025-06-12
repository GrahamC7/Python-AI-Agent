import os

def write_file(working_directory, file_path, content):
    try:
        working_directory = os.path.abspath(working_directory)
        if os.path.isabs(file_path):
            abs_file_path = os.path.abspath(file_path)
        else:
            abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # ensure the file is within the working directory
        if not os.path.commonpath([working_directory, abs_file_path]) == working_directory:
            return f'Error: Cannot write to "{abs_file_path}" as it is outside the permitted directory'
        
        # create parent directories if they do not exist
        parent_dir = os.path.dirname(abs_file_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        # overwrite the contents of the file with the content argument
        with open(abs_file_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'