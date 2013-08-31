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



##############################################################################
def not_main():
    global _anagrams
    global _len_values
    for word in Constants.words:
        value = _calc_value(word)
        _anagrams[value].append(word)
        len_word = len(word)
        _len_values[len(word)][value].append(word)



