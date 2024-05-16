from common_func import LANG
import common_func
import os
import json
import shutil
import datetime
import update_hash

def get_file_list(target_dir_path: str, file_extension: str) -> list:
    """
    Retrieves a list of files with a specific file extension in the target directory.

    Args:
        target_dir_path (str): The path to the target directory.
        file_extension (str): The desired file extension.

    Returns:
        list: A list of file paths with the specified file extension in the target directory.

    Example:
        >>> get_file_list('/path/to/directory', '.txt')
        ['/path/to/directory/file1.txt', '/path/to/directory/file2.txt']
    """
    
    if os.path.exists(target_dir_path) and os.path.isdir(target_dir_path):
        ttf_files = [os.path.join(target_dir_path, file) for file in os.listdir(target_dir_path) if file.endswith(file_extension)]
        return ttf_files
    else:
        print("The '" + target_dir_path + "' folder does not exist or is not a directory.")
        return []

def update_non_english_data(english_data, non_english_data, use_english_transcript):
    def traverse_and_update(eng_dict, non_eng_dict):
        for key, value in eng_dict.items():
            if isinstance(value, dict):
                if key not in non_eng_dict or not isinstance(non_eng_dict[key], dict):
                    non_eng_dict[key] = {}
                traverse_and_update(value, non_eng_dict[key])
            elif key not in non_eng_dict:
                if use_english_transcript:
                    non_eng_dict[key] = value
                else:
                    non_eng_dict[key] = ""
            elif non_eng_dict[key] == "" and use_english_transcript:
                non_eng_dict[key] = value
            elif non_eng_dict[key] == value and not use_english_transcript:
                non_eng_dict[key] = ""

    traverse_and_update(english_data, non_english_data)
    return non_english_data

def update_target(en_file, t_file, use_english_transcript):
    with open(en_file, 'r', encoding='utf-8') as english_file:
        english_data = json.load(english_file)
    
    try:
        with open(t_file, 'r', encoding='utf-8') as target_file:
            target_data = json.load(target_file)
    except FileNotFoundError:
        target_data = {}
    
    updated_non_english_data = update_non_english_data(english_data, target_data, use_english_transcript)

    # Write updated non-English JSON back to file
    if not os.path.exists(t_file):
        os.makedirs(os.path.dirname(t_file), exist_ok=True)
    
    with open(t_file, 'w', encoding='utf-8') as non_english_file:
        json.dump(updated_non_english_data, non_english_file, indent=4, ensure_ascii=False)



def update_target_files(en_files, target_files, use_english_transcript, target_language):
    # Create the timestamp before the loop
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")

    for en_file, target_file in zip(en_files, target_files):
        # Define the backup directory inside the loop
        backup_dir = f'{os.path.dirname(target_file)}/backup_{target_language}/{timestamp}'
        # Create a backup before updating the target file
        if not os.path.exists(target_file):
            print(f"Creating a new file for {os.path.basename(target_file)}")
        else:
            print(f"Updating {os.path.basename(target_file)}")
            os.makedirs(backup_dir, exist_ok=True)
            print(f"creating backup:{backup_dir}/{os.path.basename(target_file)}")
            shutil.copy(target_file, f'{backup_dir}/{os.path.basename(target_file)}')

        # Update the target file
        update_target(en_file, target_file, use_english_transcript)

def ask_if_insert_english_transcript():
    while True:
        user_input = input("\nFor English elements that are not present in the target transcript you are trying to update,\n"
                           "do you want to: \n"
                           "0: insert an empty string\n"
                           "or \n"
                           "1: insert English transcript?\n"
                           "Enter 0 for empty string and 1 for English transcript: ")
        if user_input == '1':
            return True
        elif user_input == '0':
            return False
        else:
            print("Invalid input. Please enter 1 for yes or 0 for no.")

def get_target_json_paths(english_json_file_paths, target_language):
    """
    This function generates and returns the relative paths for the target language's JSON files.

    It first creates the necessary directories if they do not exist. Then, for each English JSON file path,
    it generates the corresponding target language JSON file path by replacing '_en' with the target's language code
    in the filename, and appends it to the list of target JSON file paths.

    Args:
        english_json_file_paths (list): A list of full paths for the English JSON files.
        target_language (str): The target language for the transcripts.

    Returns:
        target_json_full_paths (list): A list of relative paths for the target language JSON files.
    """
    target_dir_path = "../draft/" + target_language
    common_func.create_directories_if_not_exist(output_dir_base=target_dir_path)
    target_json_full_paths = []
    for en_json_full_path in english_json_file_paths:
        target_json_full_paths.append("../draft/" + target_language + "/" + (os.path.basename(en_json_full_path)).replace("_en","_" + target_language))
    return target_json_full_paths

def get_target_language():
    """
    This function prompts the user to select a target language from a list of languages.

    It first prints a list of languages with corresponding numbers. Then, it asks the user to enter
    a number corresponding to the language they wish to update/create transcript files for. It returns
    the selected language.

    Args:
        LANG (list): A list of languages.

    Returns:
        target_language (str): The selected target language.
    """
    while True:
        print("Enter a number:")
        print("0 for every languages")
        for i, lang in enumerate(LANG):
            print(f"{i+1} for {lang}")
        target_language_num = input("For the language you wish to update/create transcript files: ")
        if target_language_num.isdigit() and int(target_language_num) < len(LANG) + 1 and int(target_language_num) > -1:
            if int(target_language_num) == 0:
                return 0
            else:
                target_language = LANG[int(target_language_num)-1]
                return target_language
        else:
            print("Invalid input. Please enter a valid number.")

if __name__ == '__main__':
    print('tip: use ctr-c to force exit')
    english_dir_path = "../draft/en"
    english_json_file_paths = get_file_list(english_dir_path, ".json")   

    target_language = get_target_language()
    
    use_english_transcript = ask_if_insert_english_transcript()
    if target_language == 0:
        for l in LANG:
            target_json_full_paths = get_target_json_paths(english_json_file_paths, l)
            update_target_files(english_json_file_paths, target_json_full_paths, use_english_transcript, l)
    else:
        target_json_full_paths = get_target_json_paths(english_json_file_paths, target_language)
        update_target_files(english_json_file_paths, target_json_full_paths, use_english_transcript, target_language)
    
    print('\nupdating hash files for all languages')
    update_hash.main()