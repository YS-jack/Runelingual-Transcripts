# RuneLingual English transcript provider
Follow these steps to create or update the Database needed to run RuneLingual.

## Updating the English transcript
You need to know how to run a Python program, and also an environment run one. After that is done,
1. Clone this repository. 
2. To update the English transcripts with data on wiki/chisel, run [main_generate_English_transcript.py](./main_generate_English_transcript.py) with the option *-updateAll*
2. The data included in the wiki/chisel are:
    - Name, exmaine, option of items, npcs, objects
    - Dialogues/Overhead texts with npcs and pets
    - Level up messages

## Adding Other Data Manually
If trying to add new data that is **not** included in the wiki/chisel database, you need to create a TSV or add to existing TSV (tab separated values) files in [./manual_data](./manual_data/). 
- when creating a new TSV file, the first line should be column names, then from 2nd line write the data you wish to add. (see already existing TSV files, or reach out on discord)

1. run [jsonHandler.py](./jsonHandler.py)

All data in English should have been added to [transcript.db](./transcript.db). To view its content, download SQL viewer such as [SQLite browser](https://sqlitebrowser.org).


