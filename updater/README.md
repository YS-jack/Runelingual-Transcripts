# RuneLingual Transcript Updater

Welcome to the updater directory of the RuneLingual Transcript Sources. This directory contains scripts and utilities to update and maintain the transcripts used by the RuneLingual plugin.

## Overview of Updater Programs

The `Updater` directory contains five distinct programs, each designed to perform specific tasks for maintaining and updating transcripts. Below is a detailed description of each program's functionality:

1. [`main_generate_English_transcript.py`](update_english_transcript/main_generate_English_transcript.py): This program is responsible for updating the English transcript from the source. Read the [explanation](update_english_transcript/readme.md) for more detail.

2. [`update_nonEn_transcripts.py`](./update_nonEn_transcripts.py): This program reads data from the [English transcript database](transcript.db), and updates all other language's transcript to include records that are not included in that those files. If a translation file doesn't exist, it will create a copy of the English transcript, and add a column for translation

3. [`update_char_images.py`](./update_char_images.py): This program creates character images for insertion like emojis in the RuneLite client. This is particularly useful for languages whose alphabets differ significantly from English and cannot be displayed directly through conventional means.

4. [`update_hash.py`](./update_hash.py): This program generates hash files for all languages. These hash files are crucial for the RuneLingual plugin to determine if the local file is current.


For a deeper understanding of why these scripts are essential, please refer to the [README](./RuneLingual/transcript/README.md) in the top directory.

## How to create a Transcript for New Language

Firstly clone this repository, and install python to your system. (ask Chat-GPT for mor info, it's very informative!)
Then, to add a new language, simply run the programs in the order listed above (1-4).

Program 3 [`update_char_images.py`](./update_char_images.py) is unnecessary if the language uses the English alphabet, including characters with accents (like those in Spanish, Portuguese, Norwegian). But for languages such as Japanese, Russian, it must be configured and ran. If you're unsure, ask one of our developers and we'll be able to test it for you.

## How to Update Foriegn Transcripts After an OSRS Update
Firstly clone this repository, and install python to your system. (ask Chat-GPT for mor info, it's very informative!)
Then, to update transcripts in language other than English, run program [1](update_english_transcript/main_generate_English_transcript.py), [2](./update_nonEn_transcripts.py) and [4](./update_hash.py).

If the English transcript is already up to date, run program [2](./update_nonEn_transcripts.py) and [4](./update_hash.py).

## What to Do after Obtaining a Transcript
After cloning this repository and executing some codes, inside the [draft folder](../draft/), there should be a transcript for each language stated in [common_func.py](common_func.py).

The transcript file will be in Excel format. You can simply start adding translations in the language's column.

After you've made progress and want to update the plugin, you can either send the file to one of the developers in our [Discord server](https://discord.gg/ehwKcVdBGS), or add the language's folder in [draft folder](../draft/) and make a pull request to the GitHub repository.

## Developers: after receiving translated transcript
1. Clone the whole repository to your local machine
2. Run translatedExcel_to_TSV.py
3. Check inside the target language in [draft folder](../draft/) that there is a TSV version of the newly obtained translation.
4. Copy the TSV version to the language's folder in [public folder](../public/). If it already exists, replace it.
5. Check that no files have been deleted in other languages' folder.
6. After you are sure correct files are in each folder of [public folder](../public/), make a pull request, and have someone accept it.


## Contributing

We welcome contributions to improve our updater scripts. If you'd like to contribute, please refer to the main [README.md](../README.md) file for more information.

## Let's Chat!

Need a hand or have a question? Join us on our [Discord server](https://discord.gg/ehwKcVdBGS). We're here to help and love hearing from you!

## License

This project is licensed under the [MIT License](../LICENSE).
