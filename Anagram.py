#!/usr/bin/python3

## python modules
import collections
import sys
from optparse import OptionParser

## my modules
import Constants
import dwanderson

ANAGRAMS = collections.defaultdict(set)
LEN_VALUES = collections.defaultdict(lambda: collections.defaultdict(set))
WORDS = set() ## filled in differently if main() or not_main()

##############################################################################
def _calc_value(letters):
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
    for lett in letters:
        value *= Constants.PRIMEABET[lett]
    return value


@dwanderson.time_me
def looping_anagram(letters, nwords=1, MIN=3):
    """ Find anagrams of a given set of letters. If only one anagram is desired
        it is a look-up in a precomputed table. If more than one anagram is
        requested, it iteratively considers every possible splitting of
        letters, checking each for anagrams, that are at least MIN letters 
        long, which defaults to 3.
        Appropriate doctests under looping_anagram()
        >>> looping_anagram("AEGLLRY")
        ['ALLERGY', 'GALLERY', 'LARGELY', 'REGALLY']

        >>> looping_anagram("GOLFJUMP", 2)
        ['FLOG JUMP', 'FLUMP JOG', 'GOLF JUMP']

        >>> looping_anagram("GOLFJUMP", 2, 4)
        ['FLOG JUMP', 'GOLF JUMP']
    """
    letters = "".join(l.upper() for l in letters if l.isalpha())
    if nwords == 1:
        return ANAGRAMS[_calc_value(letters)]
    already_seen = set()
    anagrams = set()
    nletts = len(letters)
    maxIters = 2 ** (nletts - 1)
    for itr in range(maxIters):
        word1 = ""
        word2 = ""
        for pos in range(nletts):
            if (2**pos) & itr:
                word1 += letters[pos]
            else:
                word2 += letters[pos]
        if word1 in already_seen or word2 in already_seen:
            continue
        already_seen.update([word1, word2])
        if len(word1) < MIN or len(word2) < (MIN * (nwords - 1)):
            continue
        anagram1 = ANAGRAMS[_calc_value(word1)]
        if not anagram1:
            continue
        anagram2 = looping_anagram(word2, nwords-1, time_me=False)
        for a1 in anagram1:
            for a2 in anagram2:
                ordered = " ".join(sorted((a1 + " " + a2).split(" ")))
                anagrams.add(ordered)
    return anagrams


    return anagrams


##############################################################################
@dwanderson.time_me
def not_main():
    global ANAGRAMS
    global LEN_VALUES
    global WORDS
    WORDS = dwanderson.readin_words()
    for word in WORDS:
        value = _calc_value(word)
        ANAGRAMS[value].add(word)
        LEN_VALUES[len(word)][value].add(word)


##############################################################################
if __name__ == '__main__':
    main()
else:
    not_main()
