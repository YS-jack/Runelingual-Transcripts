from common_func import LANG
import common_func
import os
import json


def get_file_list(target_dir_path:str, file_extension:str) -> list: 
    # Check if the "fonts" folder exists
    if os.path.exists(target_dir_path) and os.path.isdir(target_dir_path):
        # Get a list of all files in the "fonts" folder ending with ".ttf"
        ttf_files = [os.path.join(target_dir_path,file) for file in os.listdir(target_dir_path) if file.endswith(file_extension)]
        return ttf_files
    else:
        print("The '" + target_dir_path + "' folder does not exist or is not a directory.")
        return []

def update_non_english_data(english_data, non_english_data):
    def traverse_and_update(eng_dict, non_eng_dict):
        for key, value in eng_dict.items():
            if isinstance(value, dict):
                if key not in non_eng_dict or not isinstance(non_eng_dict[key], dict):
                    non_eng_dict[key] = {}
                traverse_and_update(value, non_eng_dict[key])
            elif key not in non_eng_dict:
                non_eng_dict[key] = ""

    traverse_and_update(english_data, non_english_data)
    return non_english_data

def update_target(en_file, t_file):
    with open(en_file, 'r', encoding='utf-8') as english_file:
        english_data = json.load(english_file)
    
    try:
        with open(t_file, 'r', encoding='utf-8') as target_file:
            target_data = json.load(target_file)
    except FileNotFoundError:
        target_data = {}
    
    updated_non_english_data = update_non_english_data(english_data, target_data)

    # Write updated non-English JSON back to file
    if not os.path.exists(t_file):
        os.makedirs(os.path.dirname(t_file), exist_ok=True)
    
    with open(t_file, 'w', encoding='utf-8') as non_english_file:
        json.dump(updated_non_english_data, non_english_file, indent=4, ensure_ascii=False)

def update_target_files(en_files, target_files):
    for en_file, target_file in zip(en_files, target_files):
        update_target(en_file, target_file)

if __name__ == '__main__':
    english_dir_path = "../draft/en"
    english_json_file_paths = get_file_list(english_dir_path, ".json")   

    print("enter a number;")
    for i, lang in enumerate(LANG):
        print(f"{i} for {lang}")
    target_language_num = int(input("for the language you wish to update/create transcript files: "))
    target_language = LANG[target_language_num]

    target_dir_path = "../draft/" + target_language
    common_func.create_directories_if_not_exist(output_dir_base=target_dir_path)
    target_json_full_paths = []
    for en_json_full_path in english_json_file_paths:
        target_json_full_paths.append("../draft/" + target_language + "/" + (os.path.basename(en_json_full_path)).replace("_en","_" + target_language))

    update_target_files(english_json_file_paths, target_json_full_paths)