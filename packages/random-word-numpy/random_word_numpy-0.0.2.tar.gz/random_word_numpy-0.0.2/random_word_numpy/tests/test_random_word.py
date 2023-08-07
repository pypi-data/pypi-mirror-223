from unittest import TestCase, main
from random_word_numpy import get_random_words, get_random_word
import numpy as np


class TestRandomWord(TestCase):
    # using single instance for all tests

    rng = np.random.default_rng(2021)

    def test_get_random_word(self):
        word = get_random_word(np_generator=self.rng)
        assert word == "scholarlike"

    def test_get_random_words(self):
        words = get_random_words(2, np_generator=self.rng)
        assert words == ['schillings', 'mesothermal']


if __name__ == "__main__":
    main()
