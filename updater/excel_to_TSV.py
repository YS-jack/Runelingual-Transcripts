import pandas as pd
import os
import common_func
import update_hash

def xlsx_to_tsv(xlsx_file_path, target_dir, columns=None):
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
		tsv_filename = os.path.join(output_dir, f"{sheet_name}.tsv")
		
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
	xlsx_to_tsv(xlsx_file_path, draft_lang_dir, columns=columns)

def main():
    print('tip: use ctr-c to force exit')
    target_lang_code = common_func.get_target_language()
    if target_lang_code == 0:
	    for lang in common_func.LANG:
	        oneExcel_to_manyTSV(lang)
    else:
        oneExcel_to_manyTSV(target_lang_code)
	
    update_hash.main()

if __name__ == "__main__":
	main()