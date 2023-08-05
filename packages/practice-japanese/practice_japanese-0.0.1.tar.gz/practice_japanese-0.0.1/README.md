# practice_japanese

A simple flashcard program to help practice Japanese characters. Per-character statistics are collected and summarized.

## Requirements

- Python3.6+

## Installation

```bash
sudo python3 setup.py install
```

This will create a CLI called `practice_japanese` on your PATH.

Alternatively, install via pip:

```bash
python3 -m pip install practice_japanese
```

## Usage

```bash
practice_japanese [--character-set CHARACTER_SET] [--statistics-file STATISTICS_FILE]
```

Characters from the selected character set will be displayed; the user is expected to enter the romaji for each character.

By default, the full character set will be used.

Press `CTRL+C` to exit; statistics for your slowest and least accurate characters (and the characters you commonly mix them up with) will be printed. These statistics are for your entire history of practicing, not the current session.

By default, character statistics will be saved to `character_stats.json` in your `pwd`. These statistics are updated each time you practice.
