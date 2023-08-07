from numpy.random import choice
from json import load
from os.path import dirname, join


class Local(object):
    def __init__(self):
        self.source = join(dirname(__file__), "..", "database", "words.json")

    def get_random_word(self):
        with open(self.source) as word_database:
            valid_words = load(word_database)
        return choice(list(valid_words.keys()))

    def get_random_words(self, size=None):
        with open(self.source) as word_database:
            valid_words = load(word_database)
        return list(choice(list(valid_words.keys()), size=size))
