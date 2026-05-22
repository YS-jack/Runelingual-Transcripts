import os
import common_func
import pandas as pd
import shutil
from datetime import datetime

def create_backup(file_path):
    directory, filename = os.path.split(file_path)
    file_name_no_ext, file_extension = os.path.splitext(filename)
    backup_dir = os.path.join(directory, 'backup')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"{file_name_no_ext}_{datetime_str}{file_extension}"
    backup_file_path = os.path.join(backup_dir, backup_filename)
    shutil.copy(file_path, backup_file_path)
    print(f"Backup created: {backup_file_path}")

def remove_duplicate_dialogue(target_lang_code):
    draft_dir = common_func.DRAFT_DIR
    draft_lang_dir = os.path.join(draft_dir, target_lang_code)
    file_path = os.path.join(draft_lang_dir, f"transcript_{target_lang_code}.xlsx")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Processing: {file_path}")
    create_backup(file_path)

    # Read all sheets into memory first
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names

    if 'dialogue' not in sheet_names:
        print("No 'dialogue' sheet found in the file.")
        return

    all_sheets_data = {}
    for sheet in sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        if sheet == 'dialogue':
            original_count = len(df)
            df = df.drop_duplicates(subset=['english'], keep='first')
            removed_count = original_count - len(df)
            print(f"dialogue sheet: removed {removed_count} duplicate rows")
        all_sheets_data[sheet] = df

    # Close the reader before writing
    del xls

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for sheet in sheet_names:
            all_sheets_data[sheet].to_excel(writer, sheet_name=sheet, index=False)

    print("Done!")

def main():
    print('tip: use ctr-c to force exit')
    print('This script removes duplicate English entries from the dialogue sheet\nof the transcript_{lang}.xlsx file.')

    target_lang_code = common_func.get_target_language()
    if target_lang_code == 0:
        print("Cannot process all languages at once")
        return

    remove_duplicate_dialogue(target_lang_code)

if __name__ == "__main__":
    main()
