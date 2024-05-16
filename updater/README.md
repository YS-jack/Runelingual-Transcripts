# RuneLingual Transcript Updater

Welcome to the updater directory of the RuneLingual Transcript Sources. This directory contains scripts and utilities to update and maintain the transcripts used by the RuneLingual plugin.

## Overview of Updater Programs

The `Updater` directory contains five distinct programs, each designed to perform specific tasks for maintaining and updating transcripts. Below is a detailed description of each program's functionality:

1. [`update_En_transcript.java`](./update_En_transcripts.java): This program is responsible for updating the English transcript from the source.

2. [`update_nonEn_transcripts.py`](./update_nonEn_transcripts.py): This program enriches non-English transcripts by adding JSON key-value pairs that exist in the English transcripts but are absent in other languages' transcripts. It provides the user with the option to populate the new values with either an empty string or the original English string prior to updating the transcripts.

3. [`update_char_images.py`](./update_char_images.py): This program creates character images for insertion like emojis in the RuneLite client. This is particularly useful for languages whose alphabets differ significantly from English and cannot be displayed directly through conventional means.

4. [`update_hash.py`](./update_hash.py): This program generates hash files for all languages. These hash files are crucial for the RuneLingual plugin to determine if the local file is current.

5. [`switch_English_and_emptyString.py`](./switch_English_and_emptyString.py): This program modifies an existing transcript file by either replacing all instances of an empty string ("") with the original English string or vice versa.

For a deeper understanding of why these scripts are essential, please refer to the [README](./RuneLingual/transcript/README.md) in the top directory.

# Steps for Adding a New Language

Follow these steps to add a new language:

1. Run the programs in the order listed above (1-4).

    - Program 3 [`update_char_images.py`](./update_char_images.py) is unnecessary if the language uses the English alphabet, including characters with accents (like those in Spanish, Portuguese, Norwegian). If you're unsure, ask one of our developers and we'll be able to test it for you.

2. Use [`switch_English_and_emptyString.py`](./switch_English_and_emtpyString.py) if you wish to switch between English and an empty string ("") for untranslated values.

## What to Do After New Items/NPCs etc. Are Added

Use programs 1, 2, 4 in this order. It's recommended that all non-English transcripts should be up-to-date before doing this, or you're likely to encounter problems when merging changes.

## How to Run programs in the Updater

Follow these steps to use the updater:

1. Get a GitHub account if you don't have one already and login.
2. Fork this repository to your own account.
3. Clone the repository to your local machine.
4. Set up an environment to run Python.
5. Run the desired script in this directory.
6. Input as the prompt requires.
7. Stage your changes with `git add .`.
8. Commit your changes with `git commit`.
9. Push your changes with `git push`.
10. Create a pull request from the webpage of your fork to the main RuneLingual repository.
11. Wait for someone to review and merge it.

## Contributing

We welcome contributions to improve our updater scripts. If you'd like to contribute, please refer to the main [README.md](../README.md) file for more information.

## Let's Chat!

Need a hand or have a question? Join us on our [Discord server](https://discord.gg/ehwKcVdBGS). We're here to help and love hearing from you!

## License

This project is licensed under the [MIT License](../LICENSE).
