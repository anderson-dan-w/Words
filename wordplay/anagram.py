from __future__ import print_function, division, absolute_import
import collections
import os
import sys
import operator

from wordplay import constants

if sys.version_info.major == 3:
    from functools import reduce

WORDS = set()
ANAGRAMS = collections.defaultdict(set)
LEN_VALUES = collections.defaultdict(lambda: collections.defaultdict(set))
EMPTY = ""


def _calc_value(letters):
    """ Calculate a unique value for a given string, which is presumed to be
        comprised of only upper-case letters. Violating this fails silently,
        giving the caller 0 in return.
    """
    return reduce(operator.mul, (constants.PRIMEABET[l] for l in letters), 1)


def precalculate_values():
    for word in WORDS:
        value = _calc_value(word)
        ANAGRAMS[value].add(word)
        LEN_VALUES[len(word)][value].add(word)


def readin_words():
    text_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "texts")
    texts = [os.path.join(text_dir, f) for f in os.listdir(text_dir)]
    for fname in [f for f in texts if f.endswith(".dict")]:
        with open(fname) as fh:
            text = str(fh.read()).replace("\r", "\n")
        words = (w for w in text.upper().split("\n") if w)
        WORDS.update(words)
    precalculate_values()


def normalize_letters(letters):
    return EMPTY.join(l.upper() for l in letters if l.isalpha())


def generate_str_splits(letters):
    letters = normalize_letters(letters)
    n_letters = len(letters)
    max_combos = 2**(n_letters - 1)
    for number in range(max_combos):
        word1, word2 = EMPTY, EMPTY
        for index, letter in enumerate(letters):
            if (2**index) & number:
                word1 += letter
            else:
                word2 += letter
        yield word1, word2


def anagram(letters, nwords=1, MIN=3):
    """ Find anagrams of a given set of letters. If only one anagram is desired
        it is a look-up in a precomputed table. If more than one anagram is
        requested, it iteratively considers every possible splitting of
        letters, checking each for anagrams, that are at least MIN letters
        long, which defaults to 3.
    """
    if nwords == 1:
        return ANAGRAMS[_calc_value(normalize_letters(letters))]
    anagrams = set()
    already_seen = set()
    for word1, word2 in generate_str_splits(letters):
        if word1 in already_seen or word2 in already_seen:
            continue
        already_seen.update({word1, word2})
        if len(word1) < MIN or len(word2) < (MIN * (nwords - 1)):
            continue
        anagram1 = ANAGRAMS[_calc_value(word1)]
        if not anagram1:
            continue
        anagram2 = anagram(word2, nwords - 1)
        for a1 in anagram1:
            for a2 in anagram2:
                ordered = " ".join(sorted((a1 + " " + a2).split(" ")))
                anagrams.add(ordered)
    return anagrams


def anagram_with_fewer(letters, MIN=3):
    anagrams = set()
    for word1, word2 in generate_str_splits(letters):
        if len(word1) >= MIN:
            anagrams.update(anagram(word1))
        if len(word2) >= MIN:
            anagrams.update(anagram(word2))
    return anagrams


def anagram_plus(letters, nblanks=1, nwords=1, MIN=3, start=0):
    if isinstance(start, str):
        start = constants.ALPHABET.index(start.upper())
    answer_dict = collections.defaultdict(set)
    if nblanks == 0:
        answer_dict[""].update(anagram(letters, nwords, MIN))
        return answer_dict
    for letter in constants.ALPHABET[start:]:
        new_string = letters + letter
        tmp_dict = anagram_plus(new_string, nblanks - 1, nwords, MIN, letter)
        for k, v in tmp_dict.items():
            if not v:
                continue
            key = "".join(sorted(list(letter + k)))
            answer_dict[key].update(v)
    return answer_dict


def anagram_plus_with_fewer(letters, nblanks=1, MIN=3, start=0):
    if isinstance(start, str):
        start = constants.ALPHABET.index(start.upper())
    answer_dict = collections.defaultdict(set)
    if nblanks == 0:
        answer_dict[""].update(anagram_with_fewer(letters, MIN))
        return answer_dict
    for letter in constants.ALPHABET[start:]:
        new_string = letters + letter
        tmp_dict = anagram_plus_with_fewer(new_string, nblanks - 1, MIN, letter)
        for k, v in tmp_dict.items():
            if not v:
                continue
            key = "".join(sorted(list(letter + k)))
            answer_dict[key].update(v)
    return answer_dict


##############################################################################
def get_panvowellic(plus_y=False, only_once=True):
    anagrams = set()
    str_vowels = "AEIOU" + ("Y" if plus_y else EMPTY)
    vowels = 1
    multi_vowels = []
    for v in str_vowels:
        vowels *= constants.PRIMEABET[v]
        multi_vowels.append(constants.PRIMEABET[v] ** 2)
    for value, anagram_list in ANAGRAMS.items():
        if value % vowels:
            continue
        ## value % mv is non-zero, i.e. True, if it doesn't divide evenly,
        ## meaning there are not 2 of that vowel; so need all to be True
        if only_once and not all(value % mv for mv in multi_vowels):
            continue
        anagrams.update(anagram_list)
    return anagrams


if __name__ != '__main__':  # pragma: no cover
    readin_words()
