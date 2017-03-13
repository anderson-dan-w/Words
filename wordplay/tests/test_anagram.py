import unittest
import collections

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

    def test_normalize_letters(self):
        ## most basic assertion
        self.assertEqual("A", A.normalize_letters("A"))
        ## prove it capitalizes
        self.assertEqual("A", A.normalize_letters("a"))
        ## prove it ignores numbers, punctuation, spaces
        self.assertEqual("A", A.normalize_letters("A 3?"))

    def test_generate_str_splits(self):
        letters = "ABC"
        expected = [
            ("", "ABC"),
            ("A", "BC"),
            ("B", "AC"),
            ("AB", "C")
        ]
        observed = list(A.generate_str_splits(letters))
        self.assertEqual(expected, observed)

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

    def test_anagram_with_fewer(self):
        letters = "CATS"
        expected_contains = {"CAT", "ACT", "SAT"}
        observed = A.anagram_with_fewer(letters)
        for expected in expected_contains:
            self.assertIn(expected, observed)

    def test_anagram_plus(self):
        letters = "JNX"
        expected = collections.defaultdict(set)
        expected["I"].add("JINX")
        observed = A.anagram_plus(letters)
        self.assertEqual(expected, observed)

    def test_anagram_plus_with_fewer(self):
        letters = "JNX"
        expected = collections.defaultdict(set)
        expected["I"].update({"JIN", "JINX", "NIX"})
        expected["U"].update({"JUN"})
        observed = A.anagram_plus_with_fewer(letters)
        self.assertEqual(expected, observed)

    def test_get_panvowellic(self):
        each_once_no_y = "FACETIOUS"
        each_once_with_y = "FACETIOUSLY"
        multi_no_y = "EDUCATIONAL"
        multi_with_y = "EDUCATIONALLY"

        ## CASE 1:
        observed_once_no_y = A.get_panvowellic(plus_y=False, only_once=True)
        ## y is *allowed* but not *required* in plus_u
        for expect_in in (each_once_no_y, each_once_with_y):
            self.assertIn(expect_in, observed_once_no_y)
        ## but any vowel multiple times shouldn't be allowed
        for expect_not in (multi_no_y, multi_with_y):
            self.assertNotIn(expect_not, observed_once_no_y)

        ## CASE 2:
        observed_once_with_y = A.get_panvowellic(plus_y=True, only_once=True)
        ## y is now required
        self.assertIn(each_once_with_y, observed_once_with_y)
        ## without y, and multi, aren't allowed
        for expect_not in (each_once_no_y, multi_no_y, multi_with_y):
            self.assertNotIn(expect_not, observed_once_with_y)

        ## CASE 3:
        observed_multi_no_y = A.get_panvowellic(plus_y=False, only_once=False)
        ## y is allowed, not required, multi is allowed, not required
        for expect_in in (
                each_once_no_y, each_once_with_y, multi_no_y, multi_with_y):
            self.assertIn(expect_in, observed_multi_no_y)

        ## CASE 4:
        observed_multi_with_y = A.get_panvowellic(plus_y=True, only_once=False)
        ## y is required, multi is allowed not required
        for expect_in in (each_once_with_y, multi_with_y):
            self.assertIn(expect_in, observed_multi_with_y)
        for expect_not in (each_once_no_y, multi_no_y):
            self.assertNotIn(expect_not, observed_multi_with_y)
