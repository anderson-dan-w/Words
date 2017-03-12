import unittest

from wordplay import anagram as A


class TestAnagram(unittest.TestCase):
    def test_basic_anagram(self):
        letters = "AEGLLRY"
        expected = set(["ALLERGY", "GALLERY", "LARGELY", "REGALLY"])
        self.assertEqual(expected, A.looping_anagram(letters))
