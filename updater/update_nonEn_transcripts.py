from common_func import LANG
import common_func
import os
import update_hash
import sqlite3
import pandas as pd
from openpyxl import Workbook
from update_english_transcript import jsonHandler
import update_english_transcript.common as common
import pandas as pd
import json
import os


def read_english_transcript(db_path=common_func.TRANSCRIPT_PATH):
    conn = sqlite3.connect(db_path)
    query = 'SELECT english, category, sub_category, source, notes, wiki_url FROM transcript'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_target_excel_path(target_lang_code):
    """
    returns the target language's excel transcript file path
    """
    draft_dir = common_func.DRAFT_DIR
    draft_lang_dir = os.path.join(draft_dir, target_lang_code)
    filename = f"transcript_{target_lang_code}.xlsx"
    target_excel_path = os.path.join(draft_lang_dir, filename)
    return target_excel_path

def update_excel_transcript(target_lang_code, fill_translation_bool=False):
    """
    Update the target language's excel transcript file to contain all values in the English transcript file (transcript.db).
    If the target language's transcript file does not exist, create a new one with the English transcript values and an empty 'translation' column.
    args:
    english_df: pandas dataframe, the english transcript
    target_lang_code: str, the target language code
    """
    english_df = read_english_transcript()
    print(f'Updating {target_lang_code} excel transcript...')
    file_path = get_target_excel_path(target_lang_code)
    print(file_path)
    # Check if the file does not exist to create a new one
    if not os.path.exists(file_path):
        print('file name: ' + os.path.basename(file_path) + ' does not exist, creating...')
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Group by category
            grouped = english_df.groupby('category')
            for category, group in grouped:
                english_col_index = group.columns.get_loc('english') + 1
                if fill_translation_bool:
                    group.insert(loc=english_col_index, column='translation', value=group['english'])
                else:
                    group.insert(loc=english_col_index, column='translation', value='')
                group.sort_values(by=['category', 'sub_category'], inplace=True)
                # Use the 'category' value as the sheet name
                group.to_excel(writer, sheet_name=category, index=False)
    else:
        # Update existing file
        common_func.create_backup(file_path)
        grouped = english_df.groupby('category')
        lang_df_list = {category:pd.read_excel(file_path, sheet_name=category) for category in pd.ExcelFile(file_path).sheet_names}
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for category, group in grouped:
                print("inspecting sheet: " + category)
                lang_df = lang_df_list.get(category)
                if lang_df is None:
                    print(f"Sheet named '{category}' not found, creating a new sheet...")
                    # Optionally, create an empty DataFrame or take other actions
                    lang_df = pd.DataFrame()
                    # Insert the 'trnaslation' column, fill with English transcript if fill_translation_bool is True
                    if fill_translation_bool:
                        group.insert(loc=group.columns.get_loc('english') + 1, column='translation', value=group['english'])
                    else:
                        group.insert(loc=group.columns.get_loc('english') + 1, column='translation', value='')
    

                combined_df = pd.concat([lang_df, group], ignore_index=True)
                combined_df.drop_duplicates(subset=['english', 'category', 'sub_category', 'source'], keep='first', inplace=True)
                final_df = combined_df.sort_values(by=['category', 'sub_category'])
                final_df.to_excel(writer, sheet_name=category, index=False)

    
def main():
    """
    reads data from the [English transcript database](transcript.db), 
    and updates all other language's transcript to include records that are not included in that those files. 
    If a translation file doesn't exist, it will create a copy of the English transcript, and add a column for translation
    The name of the translation file should be transcript_<lang_code>.xlsx

    lastly it will update the hash files for all languages
    """
    print('tip: use ctr-c to force exit')
    while True:
        target_lang_code = common_func.get_target_language()
        if target_lang_code == 0:
            print("cannot update all languages' transcript at once")
        else:
            break
    
    update_excel_transcript(target_lang_code)

    


    # 
    # update_hash.main()

if __name__ == '__main__':
    main()