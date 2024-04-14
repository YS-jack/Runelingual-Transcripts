## Choose your preferred language
<div style="text-align: center;">

**Original transcripts :uk:** | [Español Argentino :argentina:](https://github.com/IaKee/Runelingual-Transcripts/tree/espanol-argentino-main) | [Português Brasileiro :brazil:](https://github.com/IaKee/Runelingual-Transcripts/tree/portugues-brasileiro-main) | [Norsk :norway:](https://github.com/IaKee/Runelingual-Transcripts/tree/norsk-main)

</div>

- These are the languages we working with and support so far. 
- If you'd like to contribute or request support for another language that isn't listed, please [contact us](#contact-us).
- Feel free to tweak our language packs to your liking. We aim to support multiple language pack variants to accommodate different preferences.

# RuneLingual Transcript Sources

Welcome to the transcript sources repository for the [RuneLingual translation plugin](https://github.com/IaKee/RuneLingual-Plugin)! This repository aims to be a [contributor hub](https://discord.gg/ehwKcVdBGS) with everything related to the main RuneLingual plugin's source files, [for the main plugin repository click here](https://github.com/IaKee/RuneLingual-Plugin).

RuneLingual is a community-maintained [plugin](https://runelite.net/plugin-hub) for the officially supported game client [RuneLite](https://runelite.net) of [OldSchool Runescape](https://oldschool.runescape.com), you can read more about them on their links. 

Our goal is to unite the community by providing accessible translations in multiple languages, ensuring that every player can enjoy the game in their preferred language.

[Contributions are greatly appreciated!](#how-can-i-contribute) 


## F.A.Q.

### What are these transcripts?

Transcript sources are files containing the text used in the game. Each file represents a different aspect of the game, such as NPC dialogues, item descriptions, and contents from many different interfaces.

They are typically stored in [JSON format](https://en.wikipedia.org/wiki/JSON), which is basically a [simple string](https://en.wikipedia.org/wiki/String_(computer_science)) with a bunch of extra symbols [mapping each original string to a new value](https://en.wikipedia.org/wiki/Hash_table), this format makes it easier to the user's machine read and modify them. 

Most of the transcripts should look something like this (i've chose Brazilian Portuguese for this example):

<div style="text-align: center;">

```json
{
    "itemexamine": {
        "arazorsharpsword": "Uma espada bem afiada.",
        "arrowswithbronzeheads": "Flechas com pontas de bronze.",
        "shortbuteffective": "Curto, mas eficiente.",
    },
    "welcomemessage": {
        "welcometooldschoolrunescape": "Boas vindas a OldSchool RuneScape!"
    }
}
```

</div>

### How does the plugin uses these transcripts?

When any object containing a string is read from the live game, its name is converted to lower case, has its spaces and puctuation removed and becomes the search key (the string on the beggining of each line on the previous example).

As an example, we came across a [bronze sword](https://oldschool.runescape.wiki/w/Bronze_sword) in our inventory, when we examine it, the game should prompt you with:
> A razor sharp sword.

After this initial text processing the key should be:
> "arazorsharpsword"

The plugin uses this key to search through its transcription files, among many different object categories to check if there is a corresponding translation for the current object, as for [the previous example](#what-are-these-transcripts), for Brazilian Portuguese we can find a corresponding string as:
> "Uma espada bem afiada.

The new string is then sent to the original widget, replacing the original text even before it is shown to the player, so they can experience the game as being in Brazilian Portuguese!

### How can i contribute?

If you would like to contribute in any way, please first consider the following:

- Joining our [community Discord server](https://discord.gg/ehwKcVdBGS) to get up to date with whats is going on with the project such as for goals, development updates and to [contact us](#contact-us) in general.
- Checking the [project issues tab](https://github.com/IaKee/Runelingual-Transcripts/issues) for ongoing and planned tasks, suggestions and new ideas, feel free to contribute with your own.

If you want to contribute improving our translations packs follow these steps:
1. [Select your working language on the top of this page](#choose-your-preferred-language), to acess its corresponding branch.
2. [Create your own fork of this repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).
3. Tweak your version to your liking.
4. [Submit a pull request with your changes](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests), so it later can be reviewed and [merged with the main branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request).

If you would like to see your language supported, but feel like you can't currently contribute, please consider reaching out to your friends and clanmates sharing this project!

As of yet we currently don't have a translation tool to recomend contributors to work with, after the initial brute data processing, it is mostly manual entries. 

> So far I highly recommend using [Visual Studio Code](https://code.visualstudio.com) with [split screen](https://stackoverflow.com/questions/40709351/visual-studio-code-how-to-split-the-editor-vertically) along with the [Sync Scroll extension](https://marketplace.visualstudio.com/items?itemName=dqisme.sync-scroll), so your workspace can look like this:
![preview](https://i.imgur.com/mMJt8jZ.png)

## Disclaimer

This repository is a part of the RuneLingual project, a third-party plugin under development. It is not affiliated with Jagex, the creators of OldSchool RuneScape or RuneLite. Use this repository at your own risk.

## Contact us

If you have any questions, suggestions, feedback, or anything else feel free to reach out on [our Discord server](https://discord.gg/ehwKcVdBGS) and please check this [project's issues tab](https://github.com/IaKee/Runelingual-Transcripts/issues) for any suggestions, questions or even complaints.
