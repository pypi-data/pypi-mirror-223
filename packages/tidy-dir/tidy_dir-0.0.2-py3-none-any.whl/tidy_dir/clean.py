import os
import shutil
from tidy_dir.config import get_config, get_source_dir


def clean_directory(directory):
    config = get_config(directory)
    source_dir = get_source_dir(directory)

    for dectination_dir, extensions in config.items():
        # Iterate over the files in the source directory
        for filename in os.listdir(source_dir):
            # Check if the file extension matches any of the specified extensions
            if any(filename.endswith(ext) for ext in extensions):
                # Create the corresponding new folder if it doesn't already exist
                normalized = os.path.normpath(dectination_dir)
                new_folder = os.path.join(source_dir, normalized)
                os.makedirs(new_folder, exist_ok=True)

                # Move the file to the new folder
                source_path = os.path.join(source_dir, filename)
                destination_path = os.path.join(new_folder, filename)
                shutil.move(source_path, destination_path)
