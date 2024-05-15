# RuneLingual Transcript Updater

Welcome to the updater directory of the RuneLingual Transcript Sources. This directory contains scripts and utilities to update and maintain the transcripts used by the RuneLingual plugin.

## How to Use the Updater

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

## What the Updater Does

The updater performs the following tasks:

After all English transcripts are prepared and updated.
1. Updates (adds) JSON key-value pairs that exist in the English transcripts but not in other languages' transcripts. The new value will be an empty string if it is at the deepest level of the JSON tree structure.
2. Creates hash files for all languages. An example can be seen in the `draft/jp` directory.
3. In the RuneLingual plugin, downloads outdated/new files in the RuneLingual transcript repository compared to the player's local files. This is done by comparing the hash files in the RuneLingual transcript repository and local files, updating files that have different hash values, and if a file is missing in the local hash file but exists in the repository's hash file, simply download it. Finally, replace the local hash file with the repository's hash file.

## Contributing

We welcome contributions to improve our updater scripts. If you'd like to contribute, please refer to the main [README.md](../README.md) file for more information.

## License

This project is licensed under the [MIT License](../LICENSE).