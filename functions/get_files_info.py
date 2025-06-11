import os

def get_files_info(working_directory, directory=None):
    try:
        # resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        if directory is not None:
            directory = os.path.abspath(directory)
        else:
            directory = working_directory

        # check if directory is within working_directory
        if not os.path.commonpath([working_directory, directory]) == working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # check if directory is a directory
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'
        
        # build directory contents string
        entries = os.listdir(directory)
        entries.sort()
        lines = [f"Contents of {directory}:"]
        for entry in entries:
            path = os.path.join(directory, entry)
            if os.path.isdir(path):
                size = os.path.getsize(path)
                lines.append(f"- {entry}: file_size={size} bytes, is_dir=True")
            else:
                size = os.path.getsize(path)
                lines.append(f"- {entry}: file_size={size} bytes, is_dir=False")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {str(e)}"