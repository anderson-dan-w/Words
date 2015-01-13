#!/usr/local/bin/python3
import collections

from general.dwanderson import readin_words
WORDS = readin_words()

def gather_triples(words=WORDS):
    """ Given a set of words, find all instances of 3 consecutive letters and
        maintain the list of all words containing that triple.
    """
    triples = collections.defaultdict(set)
    for word in words:
        if len(word) < 3:
            continue
        for i in range(len(word) - 2):
            triples[word[i:i+3]].add(word)
    return triples
triples = gather_triples()

def get_only_words_with_triple(triples=triples):
    """ Return all triples that occur in only one word
    """
    return {(t, w) for t, words in triples.items() if len(words)==1
                   for w in words}

def get_only_roots_with_triple(triples=triples):
    """ Return all triples that occur only in a single pseudo-root word, where
        a fuzzy-root-word means that all the other words in the list contain
        the fuzzy-root within them.
        
        e.g. the triple DTE only occurs in midterm and midterms; midterm is
        contained within midterms, and can be considered a fuzzy-root-word.

        NB: this isn't perfect. withhold is the root of withheld, but not the
        fuzzy-root, so this would be missed.
        NB: excludes 3-letter fuzzy-roots because they lead to (some) spurious
        results. all is contained in ball, and wall, but isn't really a
        fuzzy-root
    """
    roots_with_triples = []
    for triple, words in triples.items():
        minword = min(words, key=len)
        if len(minword) > 3 and all(minword in w for w in words):
            roots_with_triples.append((triple, words))
    return roots_with_triples
