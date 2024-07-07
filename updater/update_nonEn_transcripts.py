from common_func import LANG
import common_func
import os
import update_hash
import sqlite3
import pandas as pd
from openpyxl import Workbook


def read_english_transcript(db_path=common_func.TRANSCRIPT_PATH):
    conn = sqlite3.connect(db_path)
    query = 'SELECT english, category, sub_category, source, notes, wiki_url FROM transcript'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def update_language_transcripts(english_df, target_lang_code):
    print(f'Updating {target_lang_code} transcript...')
    draft_dir = common_func.DRAFT_DIR
    draft_lang_dir = os.path.join(draft_dir, target_lang_code)

    # Check if the directory exists, and create it if it doesn't
    if not os.path.exists(draft_lang_dir):
        os.makedirs(draft_lang_dir, exist_ok=True)

    filename = f'transcript_{target_lang_code}.xlsx'
    file_path = os.path.join(draft_lang_dir, filename)

    # Check if the file does not exist to create a new one
    if not os.path.exists(file_path):
        print('file name: ' + os.path.basename(file_path) + ' does not exist, creating...')
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Group by category
            grouped = english_df.groupby('category')
            for category, group in grouped:
                english_col_index = group.columns.get_loc('english') + 1
                group.insert(loc=english_col_index, column='translation', value='')
                group.sort_values(by=['category', 'sub_category'], inplace=True)
                # Use the 'category' value as the sheet name
                
                group.to_excel(writer, sheet_name=category, index=False)
    else:
        # Update existing file
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
    target_lang_code = common_func.get_target_language()
    
    english_df = read_english_transcript()
    if target_lang_code == 0:
        for lang in LANG:
            update_language_transcripts(english_df, lang)
    else:
        update_language_transcripts(english_df, target_lang_code)

    # 
    # update_hash.main()

if __name__ == '__main__':
    main()