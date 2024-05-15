import sys
import os
import hashlib
from pathlib import Path
import zipfile
import common_func

def strip_first_directory(path):
    """Strip the first directory from the path."""
    path_obj = Path(path)
    # Create a new path without the first part
    new_path = Path(*path_obj.parts[1:])
    return new_path

def hash_file(filepath):
    """Compute SHA256 hash of the specified file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def hash_directory(directory):
    """Compute SHA256 hash for all files in a directory collectively."""
    sha256_hash = hashlib.sha256()
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'rb') as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def process_directory(lang_code):
    target_path = common_func.DRAFT_DIR + "/" + lang_code
    output_file = target_path + "/hashList_" + lang_code + ".txt"
    """Process each file and directory under the root directory."""
    files_under_target_path = common_func.get_list_files_in_directory(target_path=target_path)
    with open(output_file, 'w') as out:
        for file in files_under_target_path:
            if (os.path.basename(file) == os.path.basename(output_file)):
                continue
            filepath = os.path.join(target_path, file)
            hash_value = hash_file(filepath)
            no_first_dir = strip_first_directory(filepath)
            out.write(f"{no_first_dir}|{hash_value}\n")
            print(f"hash value for {no_first_dir} = {hash_value}")

def main():
    for lang_code in common_func.LANG:
        try:
            process_directory(lang_code)
        except FileNotFoundError:
            continue


if __name__ == "__main__":
    print(f"will generate hash for all languages in {common_func.DRAFT_DIR}")
    main()