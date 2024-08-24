import shutil
import time
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
import xml.etree.ElementTree as ET
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

def get_standard_lang_code(target_lang_code):
    """
    Convert the target language code to standard code.
    If the target language code is not in the list of standard codes, return the original code.
    """
    if target_lang_code in LANG:
        target_lang_std_code_i = LANG.index(target_lang_code)
        target_lang_std_code = common_func.LANG_CODE_STANDARD[target_lang_std_code_i]
    else:
        target_lang_std_code = target_lang_code
    return target_lang_std_code

def print_sql(conn):
    c = conn.cursor()

    # Execute a query to fetch all rows from the table
    c.execute("SELECT * FROM transcript")

    # Fetch all rows from the cursor
    rows = c.fetchall()

    # Print the rows
    for i, row in enumerate(rows):
        print(row)
        if i > 10:
            break


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
    target_lang_std_code = get_standard_lang_code(target_lang_code)
    # create a copy of the original sql dabase (.db) file
    
    shutil.copy(common_func.TRANSCRIPT_PATH, os.path.dirname(get_target_excel_path(target_lang_code)) + '/transcript_temp.db')
    # for each category in the English transcript
    for category in english_df['category'].unique():
        # if category is 'name' or 'examine', iterate through the subcategories
        sub_category_list = common.NAME_SUB_CATEGORY # todo: add subcategories of name and examine if needed
        if category in ['name', 'examine']:
            category_df_list = [english_df[(english_df['category'] == category) & 
                                (english_df['sub_category'] == sub_category)] 
                                for sub_category in sub_category_list]
            xliff_file_path_list = [get_target_excel_path(target_lang_code, extension=f'_{category}_{sub_category}.xliff') for sub_category in sub_category_list]
        else:
            category_df_list = [english_df[english_df['category'] == category]]
            xliff_file_path_list = [get_target_excel_path(target_lang_code, extension=f'_{category}.xliff')]
        
        for sub_category, xliff_file_path, category_df in zip(sub_category_list, xliff_file_path_list, category_df_list):
            # Check if the file does not exist to create a new one
            if not os.path.exists(xliff_file_path):
                print('file name: ' + os.path.basename(xliff_file_path) + ' does not exist, creating...')
                generate_xliff_transcript(category_df, target_lang_std_code, xliff_file_path)
            # Update existing file
            else:
                # get data as df from xliff file
                target_category_df = xliff_to_dataframe(xliff_file_path)
                conn = sqlite3.connect(os.path.dirname(xliff_file_path) + '/transcript_temp.db')
                c = conn.cursor()
                category_col_value = get_category_col_value(xliff_file_path)
                # iterate through the target_category_df, and if the record is found in the copy of the sql database, delete it from the db
                for index, row in target_category_df.iterrows():
                    # set query dynamically
                    query = "DELETE FROM transcript WHERE "
                    params = []
                    for col in ['english', 'category', 'sub_category', 'source']:
                        if row[col] is None:
                            query += f"{col} IS NULL AND "
                        else:
                            query += f"{col} = ? AND "
                            params.append(row[col])
                    query = query[:-5]  # Remove the last ' AND '
                    # delete records that have same values from the db
                    c.execute(query, params)
                conn.commit()
                # this will leave only the records that are not in the db
                # after that, append the remaining records to the xliff file
                
                # check if the category is name or examine, and set the query accordingly (consider sub category)
                if len(xliff_file_path_list) > 1:
                    query = 'SELECT english, category, sub_category, source, wiki_url FROM transcript WHERE category = ? AND sub_category = ?'
                    df_filtered = pd.read_sql_query(query, conn, params=(category, sub_category))
                else:
                    query = 'SELECT english, category, sub_category, source, wiki_url FROM transcript WHERE category = ?'
                    df_filtered = pd.read_sql_query(query, conn, params=(category_col_value,))

                conn.close()
                if len(df_filtered) > 0:
                    print(f'adding {len(df_filtered)} missing records to {os.path.basename(xliff_file_path)}')
                    append_df_to_xliff(xliff_file_path, df_filtered)
                else:
                    print(f'no missing records found for {os.path.basename(xliff_file_path)}')
    
    # remove the copy of the sql database
    remove_file(get_target_excel_path(target_lang_code) + '/transcript_temp.db')

def remove_file(file_path):
    if os.path.exists(file_path):
        try:
            time.sleep(3)
            os.remove(file_path)
        except PermissionError as e:
            print(f"Error deleting file {file_path}: {e}. File may be in use.")

def get_category_col_value(xliff_file_path):
    xliff_file_name = os.path.basename(xliff_file_path)
    col_name = xliff_file_name.split('_')[-1].split('.')[0]
    return col_name


def append_df_to_xliff(xliff_file_path, df_to_append):
    """
    Append records from a pandas DataFrame to an XLIFF file.
    
    Args:
    - xliff_file_path (str): Path to the XLIFF file.
    - df_to_append (pd.DataFrame): DataFrame to append to the XLIFF file.
    """
    # Parse the XLIFF file
    tree = etree.parse(xliff_file_path)
    xliff_ns = 'urn:oasis:names:tc:xliff:document:1.2'
    nsmap = {'xliff': xliff_ns}
    body = tree.find('.//xliff:body', nsmap)
    
    # Find the last trans-unit and its id
    last_trans_unit = body.findall(f".//{{{xliff_ns}}}trans-unit", nsmap)[-1]
    last_id = int(last_trans_unit.get('id')) if last_trans_unit is not None else 0


    # Iterate through each row in the DataFrame
    for index, row in df_to_append.iterrows():
        # Create a new trans-unit element with a unique ID
        trans_unit_id = str(last_id + index + 1)
        trans_unit = etree.SubElement(body, f"{{{xliff_ns}}}trans-unit", id=trans_unit_id, nsmap=nsmap)
        
        # Set the source element
        source = etree.SubElement(trans_unit, f"{{{xliff_ns}}}source", nsmap=nsmap)
        source.text = row['english']
        
        # Leave the target text empty
        target = etree.SubElement(trans_unit, f"{{{xliff_ns}}}target", nsmap=nsmap)
        
        # Set the note element with combined information
        note = etree.SubElement(trans_unit, f"{{{xliff_ns}}}note", nsmap=nsmap)
        note_text = f"category: {row.get('category', '')}\nsub_category: {row.get('sub_category', '')}\nsource: {row.get('source', '')}\nwiki_url: {row.get('wiki_url', '')}"
        note.text = note_text
    
    # Save the modified XML back to the file
    tree.write(xliff_file_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')

def xliff_to_dataframe(xliff_file_path):
    """
    Convert an XLIFF file to a pandas DataFrame.

    Args:
    - xliff_file_path (str): Path to the XLIFF file.

    Returns:
    - pd.DataFrame: DataFrame containing the extracted information.
    """
    # Load and parse the XLIFF file
    # Parse the XLIFF file
    tree = etree.parse(xliff_file_path)
    xliff_ns = 'urn:oasis:names:tc:xliff:document:1.2'
    nsmap = {'xliff': xliff_ns}
    body_element = tree.find('.//xliff:body', nsmap)
    # List to hold dictionaries for each trans-unit
    data = []

    # Iterate through each trans-unit, adjusting for namespace
    for trans_unit in body_element.findall('.//xliff:trans-unit', nsmap):
        source = trans_unit.find('.//xliff:source',nsmap).text
        translation = trans_unit.find('.//xliff:target',nsmap).text
        note = trans_unit.find('.//xliff:note',nsmap).text

        # Parse the note text
        note_dict = dict(item.split(": ", 1) for item in note.split("\n"))
        # Assuming you do something with note_dict here to add it to `data`
        
        # Create a dictionary for the current trans-unit
        trans_dict = {
            'english': source,
            'translation': translation,
            'category': note_dict.get('category',''),
            'sub_category': note_dict.get('sub_category',''),
            'source': note_dict.get('source','')
        }
        # replace 'None' to None in transdict, except 'english'
        for key, val in trans_dict.items():
            if key != 'english' and val == 'None':
                trans_dict[key] = None
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
    # Define the XLIFF namespace
    xliff_ns = "urn:oasis:names:tc:xliff:document:1.2"
    nsmap = {'xliff': xliff_ns}

    # Create the root element with the namespace
    xliff = etree.Element(f"{{{xliff_ns}}}xliff", version="1.2", nsmap=nsmap)
    file_element = etree.SubElement(xliff, f"{{{xliff_ns}}}file", **{'source-language': "en", 'target-language': target_std_lang_code, 'datatype': "plaintext", 'original': "transcript.db"})
    body = etree.SubElement(file_element, f"{{{xliff_ns}}}body")

    # Iterate through the DataFrame and create trans-unit elements
    for index, row in english_df.iterrows():
        trans_unit_id = str(index + 1)
        trans_unit = etree.SubElement(body, f"{{{xliff_ns}}}trans-unit", id=trans_unit_id)
        source = etree.SubElement(trans_unit, f"{{{xliff_ns}}}source")
        source.text = row['english']
        target = etree.SubElement(trans_unit, f"{{{xliff_ns}}}target")
        # Leave the target text empty
        note = etree.SubElement(trans_unit, f"{{{xliff_ns}}}note")
        note_text = f"category: {row['category']}\nsub_category: {row['sub_category']}\nsource: {row['source']}\nwiki_url: {row['wiki_url']}"
        note.text = note_text

    # Convert the tree to a string and write to file
    tree = etree.ElementTree(xliff)
    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding='UTF-8')


def get_update_file_type():
    while True:
        print("to update the excel transcript, enter 'e'")
        print("to update the xliff transcript, enter 'x'")
        update_type = input("Enter the type of transcript to update: ").lower()
        if update_type in ['e', 'x']:
            break
        else:
            print("Invalid input.")
    return update_type

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
    update_type = get_update_file_type()

    
    if update_type == 'e':
        update_excel_transcript(target_lang_code)
    elif update_type == 'x':
        update_xliff_transcript(target_lang_code)
    


    # 
    # update_hash.main()

if __name__ == '__main__':
    main()