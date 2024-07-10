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
from lxml import etree


def read_english_transcript(db_path=common_func.TRANSCRIPT_PATH):
    conn = sqlite3.connect(db_path)
    query = 'SELECT english, category, sub_category, source, notes, wiki_url FROM transcript'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_target_excel_path(target_lang_code, extension='.xlsx'):
    """
    returns the target language's excel transcript file path
    """
    draft_dir = common_func.DRAFT_DIR
    draft_lang_dir = os.path.join(draft_dir, target_lang_code)
    filename = f"transcript_{target_lang_code}{extension}"
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
    print(f'{target_lang_code} excel transcript updated successfully.')

def update_xliff_transcript(target_lang_code):
    """
    Update the target language's xliff transcript file to contain all values in the English transcript file (transcript.db).
    If the target language's transcript file does not exist, create a new one with the English transcript values and an empty 'translation' column.
    Creates 1 xliff file for each 'category' in the English transcript.
    args:
    target_lang_code: str, the target language code
    """
    english_df = read_english_transcript()
    print(f'Updating {target_lang_code} xliff transcript...')
    
    # convert the target language code to standard code
    if target_lang_code in common_func.LANG:
        target_lang_std_code_i = common_func.LANG.index(target_lang_code)
        target_lang_std_code = common_func.LANG_CODE_STANDARD[target_lang_std_code_i]
    else:
        target_lang_std_code = target_lang_code

    for category in english_df['category'].unique():
        category_df = english_df[english_df['category'] == category]
        file_path = get_target_excel_path(target_lang_code, extension=f'_{category}.xliff')

        # Check if the file does not exist to create a new one
        if not os.path.exists(file_path):
            print('file name: ' + os.path.basename(file_path) + ' does not exist, creating...')
            generate_xliff_transcript(category_df, target_lang_std_code, file_path)
        # Update existing file
        else:
            # get data as df from xliff file
            target_category_df = xliff_to_dataframe(file_path)
            # delete records in category_df if it has same value in columns that exist in target_category_df
            for index, row in category_df.iterrows():
                if row['english'] in target_category_df['english'].values:
                    category_df.drop(index, inplace=True) #may not be correct


def xliff_to_dataframe(xliff_file_path):
    """
    Convert an XLIFF file to a pandas DataFrame.

    Args:
    - xliff_file_path (str): Path to the XLIFF file.

    Returns:
    - pd.DataFrame: DataFrame containing the extracted information.
    """
    # Parse the XLIFF file
    tree = etree.parse(xliff_file_path)
    root = tree.getroot()
    body = root.find('{urn:oasis:names:tc:xliff:document:1.2}body')

    # List to hold dictionaries for each trans-unit
    data = []

    # Iterate through each trans-unit
    for trans_unit in body.findall('{urn:oasis:names:tc:xliff:document:1.2}trans-unit'):
        source = trans_unit.find('{urn:oasis:names:tc:xliff:document:1.2}source').text
        note = trans_unit.find('{urn:oasis:names:tc:xliff:document:1.2}note').text

        # Parse the note text
        note_dict = dict(item.split(": ", 1) for item in note.split("\n") if ": " in item)
        
        # Create a dictionary for the current trans-unit
        trans_dict = {
            'english': source,
            'category': note_dict.get('category',''),
            'sub_category': note_dict.get('sub_category',''),
            'source': note_dict.get('source','')
        }
        data.append(trans_dict)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)
    return df


def generate_xliff_transcript(english_df, target_std_lang_code, output_file):
    """
    Generate an xliff transcript file for the target language.
    The xliff file will contain all values in the English,
    relative information in note element as comment.
    
    args:
    english_df: pandas dataframe, the english transcript
    target_std_lang_code: str, the standard ISO standard code for languages (listed in common_func.py)
    """
    # Create the root element
    xliff = etree.Element('xliff', version="1.2")
    file_element = etree.SubElement(xliff, 'file', **{'source-language': "en", 'target-language': target_std_lang_code, 'datatype': "plaintext", 'original': "transcript.db"})
    body = etree.SubElement(file_element, 'body')

    # Iterate through the DataFrame and create trans-unit elements
    for index, row in english_df.iterrows():
        trans_unit = etree.SubElement(body, 'trans-unit', id=str(index + 1))
        source = etree.SubElement(trans_unit, 'source')
        source.text = row['english']
        target = etree.SubElement(trans_unit, 'target')
        # Leave the target text empty
        note = etree.SubElement(trans_unit, 'note')
        note_text = f"category: {row['category']}\nsub_category: {row['sub_category']}\nsource: {row['source']}\nwiki_url: {row['wiki_url']}"
        note.text = note_text

    # Convert the tree to a string
    tree = etree.ElementTree(xliff)
    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding='UTF-8')

def main():
    """
    reads data from the [English transcript database](transcript.db), 
    and updates all other language's transcript to include records that are not included in that those files. 
    If a translation file doesn't exist, it will create a copy of the English transcript, and add a column for translation
    The name of the translation file should be transcript_<lang_code>.xlsx

    lastly it will update the hash files for all languages
    """
    print('tip: use ctr-c to force exit')

    # ask the user whhich transcript file to update
    while True:
        target_lang_code = common_func.get_target_language()
        if target_lang_code == 0: # don't allows updating all laguages at once
            print("cannot update all languages' transcript at once")
        else:
            break

    # ask whether to update excel or xliff transcript
    while True:
        print("to update the excel transcript, enter 'e'")
        print("to update the xliff transcript, enter 'x'")
        update_type = input("Enter the type of transcript to update: ").lower()
        if update_type in ['e', 'x']:
            break
        else:
            print("Invalid input.")
    
    if update_type == 'e':
        update_excel_transcript(target_lang_code)
    elif update_type == 'x':
        update_xliff_transcript(target_lang_code)
    


    # 
    # update_hash.main()

if __name__ == '__main__':
    main()