import os
import time
import random


# Load the word list from the local `ord` file (same directory as this module).
_HERE = os.path.dirname(__file__)
_DICT_PATH = os.path.join(_HERE, "ord")

try:
    with open(_DICT_PATH, "r", encoding="utf-8") as f:
        # split on any whitespace to be forgiving about formatting
        dictionary = [w.strip() for w in f.read().split() if w.strip()]
except FileNotFoundError:
    # Fall back to empty list if the file isn't present; callers should handle this.
    dictionary = []


def get_todays_word(dictionary_list):
    date = time.strftime("%Y-%m-%d")
    random.seed(date)
    if not dictionary_list:
        return ""
    return random.choice(dictionary_list).upper()


TODAYS_WORD = get_todays_word(dictionary)

# Game configuration
ALLOWED_LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ")
ALLOWED_WORD_LENGTH = 5
ALLOWED_NUMBER_OF_GUESSES = 8
