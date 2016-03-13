import unittest

from wordplay.anagram import *

class TestAnagram(unittest.TestCase):
    def test_basic_anagram(self):
        letters = "AEGLLRY"
        expected = set(["ALLERGY", "GALLERY", "LARGELY", "REGALLY"])
        self.assertEqual(expected, looping_anagram(letters))
