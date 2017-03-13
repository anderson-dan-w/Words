import unittest

from wordplay import anagram as A


class TestAnagram(unittest.TestCase):
    def test__calc_value(self):
        a, b = "A", "B"
        a_value, b_value = A.constants.PRIMEABET[a], A.constants.PRIMEABET[b]
        aa_value = a_value * a_value
        ab_value = a_value * b_value

        ## calculate something
        self.assertEqual(a_value, A._calc_value(a))
        ## correctly calculate same letter twice
        self.assertEqual(aa_value, A._calc_value(a + a))
        ## correctly calculate different letters
        self.assertEqual(ab_value, A._calc_value(a + b))
        ## prove order doesn't matter
        self.assertEqual(ab_value, A._calc_value(b + a))

    def helper_assert_anagram_has_all_words(self):
        anagrammed_words = set()
        for word_set in A.ANAGRAMS.values():
            anagrammed_words.update(word_set)
        self.assertEqual(A.WORDS, anagrammed_words)

    def helper_assert_len_values_has_all_words(self):
        len_value_words = set()
        for anagram_dict in A.LEN_VALUES.values():
            for word_set in anagram_dict.values():
                len_value_words.update(word_set)
        self.assertEqual(A.WORDS, len_value_words)

    def test_precalculate_values(self):
        ## doesn't make sense to directly test everything; just use proxy:
        ## ensure WORDS is already populated
        self.assertNotEqual(0, len(A.WORDS))
        ## intentionally empty ANAGAMS, LEN_VALUES
        A.ANAGRAMS.clear()
        A.LEN_VALUES.clear()

        ## run the function we care about
        A.precalculate_values()
        self.helper_assert_anagram_has_all_words()
        self.helper_assert_len_values_has_all_words()

    def test_readin_words(self):
        ## clar everything out
        A.WORDS.clear()
        A.ANAGRAMS.clear()
        A.LEN_VALUES.clear()

        A.readin_words()

        ## prove readin_words() filled them all in with ...something
        self.assertNotEqual(0, len(A.WORDS))
        self.helper_assert_anagram_has_all_words()
        self.helper_assert_len_values_has_all_words()

    def test_anagram(self):
        letters = "AEGLLRY"
        expected = set(["ALLERGY", "GALLERY", "LARGELY", "REGALLY"])
        observed = A.anagram(letters)
        self.assertEqual(expected, observed)

    def test_anagram_two_words(self):
        letters = "BUG JINX"
        expected = set(["BUG JINX"])
        observed = A.anagram(letters, 2)
        self.assertEqual(expected, observed)

    def test_anagram_two_words_multiple_results(self):
        letters = "CAT JINX"
        expected = set(["ACT JINX", "CAT JINX"])
        observed = A.anagram(letters, 2)
        self.assertEqual(expected, observed)

    def test_anagram_two_words_min_length(self):
        letters = "TUSK JINX"
        ## first, ensure we get a result with default MIN length
        default_expected = set(["JINKS TUX", "JINX TUSK"])
        default_observed = A.anagram(letters, nwords=2)
        self.assertEqual(default_expected, default_observed)

        ## now, test that setting MIN excludes "TUX"
        expected = set(["JINX TUSK"])
        observed = A.anagram(letters, nwords=2, MIN=4)
        self.assertEqual(expected, observed)
