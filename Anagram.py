#!/usr/bin/python3

## python modules
import collections
from time import time

## my modules
import Constants

_start_time = time()
_anagrams = collections.defaultdict(list)
_len_values = collections.defaultdict(lambda: collections.defaultdict(list))

##############################################################################
def _calc_value(word):
    """ Calculate a unique value for a given string, which is presumed to be
        comprised of only upper-case letters. Violating this fails silently,
        giving the caller 0 in return.

    >>> _calc_value("CAB")
    30

    >>> _calc_value("ABC")
    30

    >>> _calc_value("ALLERGY")
    3029539502

    >>> _calc_value("allergy")
    0

    """
    value = 1
    for lett in word:
        value *= Constants.primeabet[lett]
    return value


def _looping_anagram(letters, howmany=1, MIN=3):
    """ Find anagrams of a given set of letters. If only one anagram is desired
        it is a look-up in a precomputed table. If more than one anagram is
        requested, it iteratively considers every possible splitting of
        letters, checking each for anagrams, that are at least MIN letters 
        long, which defaults to 3.
        Appropriate doctests under looping_anagram()
    """
    if howmany == 1:
        return _anagrams[_calc_value(letters)]
    already_seen = set()
    anagrams = set()
    len_letts = len(letters)
    maxIters = 2 ** (len_letts - 1)
    for itr in range(maxIters):
        word1 = ""
        word2 = ""
        for pos in range(len_letts):
            if (2**pos) & itr:
                word1 += letters[pos]
            else:
                word2 += letters[pos]
        if word1 in already_seen or word2 in already_seen:
            continue
        already_seen.update([word1, word2])
        if len(word1) < MIN or len(word2) < (MIN * (howmany - 1)):
            continue
        anagram1 = _anagrams[_calc_value(word1)]
        if not anagram1:
            continue
        anagram2 = _looping_anagram(word2, howmany-1)
        for a1 in anagram1:
            for a2 in anagram2:
                anagrams.add(" ".join(sorted((a1 + " " + a2).split(" "))))
    return anagrams

def looping_anagram(letters, howmany=1, MIN=3, verbose=True):
    timestart = time()
    letters = letters.replace(" ", "").upper()
    anagrams = sorted(_looping_anagram(letters, howmany, MIN))
    if verbose:
        print("Took ~%f seconds" % (time() - timestart))
    return anagrams


##############################################################################
def not_main():
    global _anagrams
    global _len_values
    for word in Constants.words:
        value = _calc_value(word)
        _anagrams[value].append(word)
        len_word = len(word)
        _len_values[len(word)][value].append(word)



