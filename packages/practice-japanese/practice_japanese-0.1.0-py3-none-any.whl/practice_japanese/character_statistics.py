from pathlib import Path
import json
from .character_sets.hiragana import *


class CharacterStatistics:
    def __init__(self, file):
        self.file = file

    def load(self):
        if Path(self.file).is_file():
            with open(self.file, "r") as f:
                data = json.load(f)
        else:
            data = {}
        self.data = data

    def update_character(self, character, correct, timedelta, wrong_char_romaji=None):
        if character in self.data:
            self.data[character]["correct"] += correct
            self.data[character]["total"] += 1
            self.data[character]["times"].append(timedelta)
            self.data[character]["average_time"] = round(
                sum(self.data[character]["times"]) / len(self.data[character]["times"]),
                2,
            )
            self.data[character]["accuracy"] = round(
                self.data[character]["correct"] / self.data[character]["total"] * 100, 2
            )
        else:
            self.data[character] = {
                "correct": correct,
                "total": 1,
                "times": [timedelta],
                "average_time": timedelta,
                "accuracy": correct / 1 * 100,
                "mixups": {},
            }

        wrong_char = reverse_hiragana.get(wrong_char_romaji, None)
        if wrong_char:
            if wrong_char in self.data[character]["mixups"]:
                self.data[character]["mixups"][wrong_char] += 1
            else:
                self.data[character]["mixups"][wrong_char] = 1

    def _get_longest_delay_characters(self):
        print()
        print("┌─────────┐")
        print("│ SLOWEST │")
        print("└─────────┘")
        for character, stats in sorted(
            self.data.items(), key=lambda x: x[1]["average_time"], reverse=True
        )[:5]:
            print(
                f"{character}\t{Hiragana.hiragana.value[character]}\t{stats['average_time']}"
            )

    def _get_least_accurate_characters(self):
        print("┌─────────────────┐")
        print("│ LOWEST ACCURACY │")
        print("└─────────────────┘")

        for character, stats in sorted(
            self.data.items(), key=lambda x: x[1]["accuracy"]
        )[:5]:
            mixups = []
            for mixup_char in sorted(stats["mixups"].keys(), reverse=True)[:3]:
                mixups.append(mixup_char)
            print(
                f"{character}\t{Hiragana.hiragana.value[character]}\t{round(stats['accuracy'])}\t{', '.join(mixups)}"
            )

    def print_stats(self):
        self._get_longest_delay_characters()
        self._get_least_accurate_characters()

    def write(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f)
