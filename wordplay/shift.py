#!/usr/bin/env python3
import collections
import itertools
import random

from general import dwanderson
from general import tools

WORDS = dwanderson.readin_words()

def _word_diff(word1, word2):
    """ Calculate the difference between two words: they are assumed to be the
        same length, though will truncate to the shorter one. They also ought
        to be the same case; generally assumed to be upper-case. This does not
        wrap around, that is, the distance between Z and A is always 25, not 1.

        >>> _word_diff("HAPPY", "HARPY")
        2

        >>> _word_diff("HAPPILY", "SADDEST")
        51

    """
    return sum(abs(ord(l1) - ord(l2)) for l1, l2 in zip(word1, word2))


def unshift(string, shifts=4, or_fewer=False):
    """ Return a list of all words that are the appropriate number of shifts
        away from the initially provided string.

        >>> d = unshift("woiefj", 10)
        >>> d[10]
        {'VOICED'}

        >>> d = unshift("woiefj", 11)
        >>> d[11]
        {'VOIDER', 'WOLFED'}

        >>> d = unshift("woiefj", 11, True)
        >>> d[9]
        ['VOIDED']
        >>> d[10]
        ['VOICED']
        >>> d[11]
        ['VOIDER', 'WOLFED']

    """
    string = string.upper()
    answers = collections.defaultdict(list)
    for word in (w for w in WORDS if len(w) == len(string)):
        diff = _word_diff(string, word)
        if (diff == shifts) or (diff < shifts and or_fewer == True):
            answers[diff].append(word)
    return answers

def random_shift(string, nshifts):
    if isinstance(string, str):
        string = list(string.upper().replace(" ",""))
    shifts = 0
    indices = [x for x in range(len(string))]
    while shifts < nshifts:
        if len(indices) == 0:
            print("only got {} shifts".format(shifts))
            break
        idx = random.randrange(0, len(indices))
        letter = string[indices[idx]]
        shift = random.randrange(1, min([nshifts - shifts + 1, 14]))
        direction = (-1) ** random.randint(0, 1)
        ascii_val = (((ord(letter) - 65) + (shift * direction)) % 26) + 65
        string[indices[idx]] = chr(ascii_val)
        shifts += shift
        indices.pop(idx)
    return "".join(string)

##############################################################################
@tools.timeme
def multi_unshift(string, shifts=4, nwords=2):
    string = string.upper()
    if nwords == 1:
        return unshift(string, shifts, True)
    answers = collections.defaultdict(list)
    for i in range(len(string) - 1):
        dict1 = unshift(string[:i], shifts, True)
        if len(dict1) == 0:
            continue
        dict2 = multi_unshift(string[i:], shifts, nwords-1)
        for k1, v1 in dict1.items():
            for k2, v2 in dict2.items():
                if k1 + k2 == shifts:
                    answers[(k1,k2)] += ([w1+" "+w2 for w1 in v1 for w2 in v2])
    return answers
