import unittest

from wordplay import anagram as A


class TestAnagram(unittest.TestCase):
    def test_looping_anagram(self):
        letters = "AEGLLRY"
        expected = set(["ALLERGY", "GALLERY", "LARGELY", "REGALLY"])
        observed = A.looping_anagram(letters)
        self.assertEqual(expected, observed)

    def test_looping_anagram_two_words(self):
        letters = "BUGJINX"
        expected = set(["BUG JINX"])
        observed = A.looping_anagram(letters, 2)
        self.assertEqual(expected, observed)

    def test_looping_anagram_two_words_multiple_results(self):
        letters = "ACIJNTX"
        expected = set(["ACT JINX", "CAT JINX"])
        observed = A.looping_anagram(letters, 2)
        self.assertEqual(expected, observed)
