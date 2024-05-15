# RuneLingual Transcripts

Welcome to the RuneLingual Transcripts project. This project contains the source files for the RuneLingual translation plugin's transcripts.

## Directory Structure

This project is organized into three main directories:

- [`public/`](./public/): This directory contains the finalized and published versions of our transcripts. These are the versions that are distributed to all RuneLingual users. Please do not make direct edits in this directory. Instead, make your edits in the "draft" directory and follow the steps outlined in the [draft directory README](draft/README.md) to publish your changes.

- [`draft/`](./draft/): This directory is where edits should be made before they're ready to be published to all RuneLingual users. Once you've made your edits and checked that there are no problems, you can copy your changes from the draft directory to the [`public`](./public) directory.

- [`updater/`](./updater/): This directory contains scripts and utilities to update and maintain the transcripts. These scripts fetch the latest transcripts from the source, compare the current transcripts with the latest versions, and update the transcripts in the public directory if necessary. For more information, please refer to the [README](./updater/README.md) in the updater directory.

## Contributing

We welcome contributions to expand our language support. If you'd like to contribute or request support for another language that isn't listed, please [contact us](#contact-us).

- If you'd like to contribute or request support for another language that isn't listed, please [contact us](#contact-us).
- Feel free to tweak our language packs to your liking. We aim to support multiple language pack variants to accommodate different preferences.

## Contact Us
For all inquiries, proposals, or contributions, don't hesitate to get in touch with us.

Should you have any queries, ideas, feedback, or other concerns, we encourage you to join [our Discord server](https://discord.gg/ehwKcVdBGS) and explore the [project's issues tab](https://github.com/IaKee/Runelingual-Transcripts/issues) for any suggestions, questions, or feedback.

## Disclaimer

This repository is associated with the [RuneLingual project](https://github.com/IaKee/RuneLingual-Plugin), an independent plugin currently under development. Please be aware that this project is not officially connected with Jagex, the developers of OldSchool RuneScape, or RuneLite.

## License

This project is licensed under the [MIT License](LICENSE).