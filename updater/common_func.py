import os
import shutil

def remove_existing_dir(directory_path, folder_name):
    # Construct the path to the folder
    folder_path = os.path.join(directory_path, folder_name)
    
    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Use shutil.rmtree to recursively delete the folder
        shutil.rmtree(folder_path)
        print(f"The folder '{folder_name}' has been deleted.")
    else:
        print(f"The folder '{folder_name}' does not exist.")

def create_directories_if_not_exist(output_dir_base):
    # Split the directory path into individual directories
    directories = output_dir_base.split("/")
    
    # Construct the full path gradually
    current_path = ""
    for directory in directories:
        current_path = os.path.join(current_path, directory)
        
        # Check if the directory exists
        if not os.path.exists(current_path):
            # Create the directory if it doesn't exist
            os.makedirs(current_path)
            print(f"Created directory: {current_path}")
        else:
            print(f"Directory already exists: {current_path}")