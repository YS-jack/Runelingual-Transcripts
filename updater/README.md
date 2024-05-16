# RuneLingual Transcript Updater

Welcome to the updater directory of the RuneLingual Transcript Sources. This directory contains scripts and utilities to update and maintain the transcripts used by the RuneLingual plugin.

## What programs in Updater Does

There are four programs in the updater directory which perform tasks to maintain and update every transcript.
Here is the description of what each programs do:
･ update_En_transcript.py : updates the English transcript from source.
･ update_nonEn_transcripts.py : adds JSON key-value pairs that exist in the English transcripts but not in other languages' transcripts. The new value can be either an empty string or the original (English) string. The user will be able to choose whether to between an empty string or the original string before the progarm updates transcripts. 
･ update_hash.py : Creates hash files for all languages. This hash file is necessary for the RuneLingual plugin to know whether the local file is up-to-date or not. An example of hash file can be seen here .


In the RuneLingual plugin, downloads outdated/new files in the RuneLingual transcript repository compared to the player's local files. This is done by comparing the hash files in the RuneLingual transcript repository and local files, updating files that have different hash values, and if a file is missing in the local hash file but exists in the repository's hash file, simply download it. Finally, replace the local hash file with the repository's hash file.

## How to Use programs in the Updater

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

## License

This project is licensed under the [MIT License](../LICENSE).
