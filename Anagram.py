#!/usr/bin/python3

## python modules
import collections
from time import time

## my modules
import Constants

_start_time = time()
_anagrams = collections.defaultdict(list)
_len_values = collections.defaultdict(collections.defaultdict)

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


