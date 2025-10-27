import os
import time
import random

ORD_LIST = os.path.dirname(__file__)
DICT_PATH = os.path.join(ORD_LIST, "ord")

try:
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        # split on whitespace
        dictionary = [w.strip() for w in f.read().split() if w.strip()]
except FileNotFoundError:
    dictionary = []


def get_todays_word(dictionary_list):
    date = time.strftime("%Y-%m-%d")
    random.seed(date)
    if not dictionary_list:
        return ""
    return random.choice(dictionary_list).upper()


TODAYS_WORD = get_todays_word(dictionary)
ALLOWED_LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ")
ALLOWED_WORD_LENGTH = 5
ALLOWED_NUMBER_OF_GUESSES = 8
