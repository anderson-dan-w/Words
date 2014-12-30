#!/usr/bin/python3
from __future__ import print_function, division

## python modules
import collections
import sys
import os
from optparse import OptionParser

## my modules
playground = os.path.dirname(os.path.realpath(__file__ + "/.."))
sys.path.append(playground)
import dwanderson
from words import constants

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
        value *= constants.PRIMEABET[lett]
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


@dwanderson.time_me
def anagram_with_fewer(letters, MIN=3):
    letters = "".join(lett.upper() for lett in letters if lett.isalpha())
    anagrams = set()
    nletts = len(letters)
    max_iters = 2 ** (nletts - 1)
    for itr in range(max_iters):
        word1 = ""
        word2 = ""
        for index in range(nletts):
            if (2 ** index) & itr:
                word1 += letters[index]
            else:
                word2 += letters[index]
        if len(word1) >= MIN:
            anagrams.update(looping_anagram(word1, time_me=False))
        if len(word2) >= MIN:
            anagrams.update(looping_anagram(word2, time_me=False))
    return anagrams


##############################################################################
@dwanderson.time_me
def plus_many(letters, nblanks=2, nwords=1, MIN=3, start=0):
    if isinstance(start, str):
        start = constants.ALPHABET.index(start.upper())
    answer_dict = collections.defaultdict(set)
    if nblanks == 0:
        answer_dict[""].update(looping_anagram(letters, nwords, MIN,
            time_me=False))
        return  answer_dict
    for lett in constants.ALPHABET[start:]:
        tmp_dict = plus_many(letters+lett, nblanks-1, nwords, MIN, lett,
                time_me=False)
        for k, v in tmp_dict.items():
            if not v:
                continue
            key = "".join(sorted(list(lett + k)))
            answer_dict[key].update(v)
    return answer_dict

@dwanderson.time_me
def plus_many_with_fewer(letters, nblanks=1, MIN=3, start=0):
    if isinstance(start, str):
        start = constants.ALPHABET.index(start.upper())
    answer_dict = collections.defaultdict(set)
    if nblanks == 0:
        answer_dict[""].update(anagram_with_fewer(letters, MIN, time_me=False))
        return answer_dict
    for lett in constants.ALPHABET[start:]:
        tmp_dict = plus_many_with_fewer(letters + lett, nblanks-1, MIN, start,
            time_me=False)
        for k, v in tmp_dict.items():
            if not v:
                continue
            key = "".join(sorted(list(lett + k)))
            answer_dict[key].update(v)
    return answer_dict


##############################################################################
##############################################################################
def panvowellic(plus_y=False, only_once=True):
    anagrams = set()
    str_vowels = "AEIOUY" if plus_y else "AEIOU"
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

USAGE = "{} <letters> [-n=nwords] [--MIN=minsize]".format(sys.argv[0])
DESCR = "Returns list of anagrams for given letters and options"
@dwanderson.time_me
def main():
    global ANAGRAMS
    global LEN_VALUES
    global WORDS
    p = OptionParser(usage=USAGE, description=DESCR)
    p.add_option('-n','--nwords', type='int', default=1,
            help='Number of words to comprise a solution, default=1')
    p.add_option('--MIN', type='int', default=3,
            help='Minimum number of letters in each anagram, default=3')
    p.add_option('-e', '--extra', type='int', default=0,
            help="number of extra, 'variable' letters to use, default=0")
    p.add_option('-s', '--start', type='str', default='A',
            help="Letter to start <--extra> letters at, default='A'")
    p.add_option('-c', '--condensed', action='store_true',
            help='Prints condensed results in the <--extra> case')
    options, args = p.parse_args()

    ## error-check input
    if len(args) != 1:
        p.error("Requires 1 positional argument, <letters>")
    letters = args[0].upper()
    nwords, MIN = options.nwords, options.MIN
    extra, start, condensed = options.extra, options.start, options.condensed
    if isinstance(start, str):
        start = constants.ALPHABET.index(start)
    if nwords * MIN > len(letters):
        p.error("nwords * MIN can't be greater than legnth of letters...")
    if any(val < 0 for val in (nwords, MIN, extra, start)):
        p.error("negative values for arguments make no physical sense")
    ## done error-checking input

    ## read in only the necessary words
    upper_limit = len(letters) + extra - (MIN * (nwords - 1))
    WORDS = dwanderson.readin_words()
    for word in WORDS:
        if nwords == 1 and len(word) != (len(letters) + extra):
            continue
        elif nwords > 1 and len(word) not in range(MIN, upper_limit+1):
            continue
        value = _calc_value(word)
        ANAGRAMS[value].add(word)
        LEN_VALUES[len(word)][value].add(word)
    ## done reading in
    
    if extra == 0:
        anagrams = looping_anagram(letters, nwords, MIN, time_me=False)
        dwanderson.print_list(anagrams)
    else:
        anagrams = plus_many(letters, extra, nwords, MIN, start, time_me=False)
        if condensed:
            anagram_set = set()
            for s in anagrams.values():
                anagram_set.update(s)
            dwanderson.print_list(anagram_set)
        else:
            dwanderson.print_dict(anagrams)

    print("Found {} answer{}".format(len(anagrams), 
                's' if len(anagrams)!= 1 else ''))
    return

##############################################################################
if __name__ == '__main__':
    main()
else:
    not_main()
