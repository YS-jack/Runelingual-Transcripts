# RuneLingual English transcript provider
Follow these steps to create or update the Database needed to run RuneLingual.

## Updating the English transcript
You need to know how to run a Python program, and also an environment run one. After that is done,
1. Clone this repository.
2. To update the English transcripts with data such as those on wiki/chisel, run [main_generate_English_transcript.py](./main_generate_English_transcript.py) with one of the following options:

### Command-Line Arguments:
- `--updateAll`: Deletes all existing English data, downloads all data from chisel and wiki, gets data from the manual files, and creates a new database.
- `--addManual`: Gets data from the manual files and updates the database without deleting existing data.
- `--addChisel`: Gets data from chisel and updates the database without deleting existing data.
- `--addWiki`: Gets data from wiki and updates the database without deleting existing data.

### Examples:
- To update everything: `python main_generate_English_transcript.py --updateAll`
- To add only manual transcripts: `python main_generate_English_transcript.py --addManual`
- To add only chisel data: `python main_generate_English_transcript.py --addChisel`
- To add only wiki data: `python main_generate_English_transcript.py --addWiki`

### Explanation of Options Other Than `--updateAll`:
- `--addManual`: This option updates the database with data from the manual files located in the `./manual_data` directory. It does not delete any existing data in the database.
- `--addChisel`: This option updates the database with data from chisel, which includes NPC, item, and object names, examines, and options. It does not delete any existing data in the database.
- `--addWiki`: This option updates the database with data from the wiki, which includes NPC dialogues. It does not delete any existing data in the database.

## Adding Other Data Manually
If trying to add new data that is **not** included in the wiki/chisel database, you need to create a TSV or add to existing TSV (tab separated values) files in [./manual_data](./manual_data/). 
- When creating a new TSV file, the first line should be column names, then from the 2nd line write the data you wish to add. (See already existing TSV files, or reach out on Discord)

## Checking the English Database
After executing, data in English should have been added to [transcript.db](../transcript.db) found under the [updater folder](..). To view its content, download an SQL viewer such as [SQLite browser](https://sqlitebrowser.org).


## Let's Chat!
Need a hand or have a question? Join us on our [Discord server](https://discord.gg/ehwKcVdBGS). We're here to help and love hearing from you!