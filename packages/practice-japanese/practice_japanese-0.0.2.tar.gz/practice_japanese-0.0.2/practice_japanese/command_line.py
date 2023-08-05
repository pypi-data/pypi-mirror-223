from sys import exit
from argparse import ArgumentParser
from .version import __version__
from datetime import datetime
from signal import signal, SIGINT
import random
from .character_statistics import CharacterStatistics
from .character_sets.hiragana import Hiragana


def main(args):
    character_set = Hiragana[args.character_set].value
    character_statistics = CharacterStatistics(args.statistics_file)
    character_statistics.load()

    def signal_handler(*args):
        character_statistics.print_stats()
        character_statistics.write()
        exit(0)

    signal(SIGINT, signal_handler)

    while True:
        before_answer = datetime.now()
        character = random.choice(list(character_set))
        answer = input(f"{character} ")
        after_answer = datetime.now()
        timedelta = round((after_answer - before_answer).total_seconds(), 2)
        if answer == character_set[character]:
            print("✓")
            character_statistics.update_character(character, 1, timedelta)
        else:
            print(f"✗ {character_set[character]}")
            character_statistics.update_character(character, 0, timedelta, answer)


def cli():
    parser = ArgumentParser(description="Practice Japanese characters")

    parser.add_argument(
        "-c",
        "--character-set",
        type=str,
        choices=Hiragana._member_names_,
        help="Which character set to practice",
        default="hiragana",
    )
    parser.add_argument(
        "-s",
        "--statistics-file",
        type=str,
        help="File to save character statistics to",
        default="character_stats.json",
    )

    args = parser.parse_args()
    main(args)
