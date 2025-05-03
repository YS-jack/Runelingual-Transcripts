import pandas as pd
import os
import common_func
import update_hash
import update_nonEn_transcripts
import csv
os.path.dirname(os.path.abspath(__file__))
from update_english_transcript import common

def xlsx_to_tsv(xlsx_file_path, target_dir, target_lang_code, columns=None):
	# Load the Excel file
	xls = pd.ExcelFile(xlsx_file_path)
	
	# Get the list of sheet names
	sheet_names = xls.sheet_names
	
	# Define the directory to save TSV files
	output_dir = target_dir
	os.makedirs(output_dir, exist_ok=True)
	
	# Iterate through each sheet in the Excel file
	for sheet_name in sheet_names:
		# Read the sheet into a pandas DataFrame
		df = pd.read_excel(xlsx_file_path, sheet_name=sheet_name)
		
		# If specific columns are provided, filter the DataFrame to include those columns only
		if columns is not None:
			df = df[columns]
		
		# Construct the TSV filename based on the Excel sheet name
		tsv_filename = os.path.join(output_dir, f"transcript_{target_lang_code}_{sheet_name}.tsv")
		
		# Save the DataFrame to a TSV file
		df.to_csv(tsv_filename, sep='\t', index=False)
		
		print(f"Saved {sheet_name} to {tsv_filename}")

def oneExcel_to_manyTSV(target_lang_code):
	draft_dir = common_func.DRAFT_DIR
	draft_lang_dir = os.path.join(draft_dir, target_lang_code)
	filename = f'transcript_{target_lang_code}.xlsx'
	xlsx_file_path = os.path.join(draft_lang_dir, filename)
	if not os.path.exists(xlsx_file_path):
		print('create the transcript with udpate_nonEn_transcripts.py first')
		print('for more information, see the README.md file in the updater directory.')
		exit(1)
	
	columns = ['english', 'translation', 'category', 'sub_category', 'source']
	xlsx_to_tsv(xlsx_file_path, draft_lang_dir, target_lang_code, columns=columns)

def xliff_to_tsv(xliff_file_path, tsv_file_path, columns=None):
	xliff_df = update_nonEn_transcripts.xliff_to_dataframe(xliff_file_path)
	if columns is not None:
		xliff_df = xliff_df[columns]
	xliff_df.to_csv(tsv_file_path, sep='\t', index=False)

	# check the csv file for english that contains 2 double quotes and start+ends with double quotes
	# if so replace the double quotes with single quotes, and remove the double quotes at the start and end of the string
	if is_file_empty(tsv_file_path):
		print(f"File {tsv_file_path} is empty. Skipping.")
		return
	with open(tsv_file_path, 'r', encoding='utf-8') as file:
		lines = file.readlines()
	updated_lines = []
	for line in lines:
		eng = line.split('\t')[0]
		if '\\""' in eng and (eng.startswith('"') and eng.endswith('"')):
			print(f"found double quotes in {eng}")
			eng = eng[1:-1].replace('\\""', '"')
			print(f"updated to {eng}")
			line = line.replace(line.split('\t')[0], eng)
		updated_lines.append(line)
	with open(tsv_file_path, 'w', encoding='utf-8', newline='') as file:
		file.writelines(updated_lines)

def manyXLIFF_to_manyTSV(target_lang_code):
	draft_dir = common_func.DRAFT_DIR
	draft_lang_dir = os.path.join(draft_dir, target_lang_code)
	xliff_files = [f for f in os.listdir(draft_lang_dir) if f.endswith('.xliff')]
	
	for xliff_file in xliff_files:
		xliff_file_path = os.path.join(draft_lang_dir, xliff_file)
		tsv_filename = os.path.splitext(xliff_file)[0] + '.tsv'
		tsv_file_path = os.path.join(draft_lang_dir, tsv_filename)

		skip = False
		for sub_cat in common.SUB_CAT_WITH_NO_EXAMINE:
			if "examine_" + sub_cat +".xliff" in xliff_file:
				skip = True
		if(skip):
			continue
		columns = ['english', 'translation', 'category', 'sub_category', 'source']
		xliff_to_tsv(xliff_file_path, tsv_file_path, columns=columns)

def is_file_empty(file_path):
    """Check if a file is empty."""
    return os.path.exists(file_path) and os.path.getsize(file_path) == 0

def get_update_file_type():
    while True:
        print("to generate tsv from excel transcript, enter 'e'")
        print("to generate from the xliff transcript, enter 'x'")
        update_type = input("Enter the type of transcript to update: ").lower()
        if update_type in ['e', 'x']:
            break
        else:
            print("Invalid input.")
    return update_type

def main():
	print('tip: use ctr-c to force exit')
	print('This program will create .tsv files from either excel or xliff files')
	target_lang_code = common_func.get_target_language()
	update_type = get_update_file_type()
	if update_type == 'e':
		if target_lang_code == 0:
			for lang in common_func.LANG:
				oneExcel_to_manyTSV(lang)
		else:
			oneExcel_to_manyTSV(target_lang_code)
	elif update_type == 'x':
		if target_lang_code == 0:
			for lang in common_func.LANG:
				manyXLIFF_to_manyTSV(lang)
		else:
			manyXLIFF_to_manyTSV(target_lang_code)
	update_hash.main()

if __name__ == "__main__":
	main()