from numpy import random
from json import load
from os.path import dirname, join


WORDS_DB = join(dirname(__file__), "database", "words.json")

def get_random_word(words_db=WORDS_DB, np_generator=None):
    with open(words_db) as word_database:
        valid_words = load(word_database)
    np_generator = np_generator or random
    return np_generator.choice(list(valid_words.keys()))

def get_random_words(size, words_db=WORDS_DB, np_generator=None):
    with open(words_db) as word_database:
        valid_words = load(word_database)
    np_generator = np_generator or random
    return list(np_generator.choice(list(valid_words.keys()), size=size))
