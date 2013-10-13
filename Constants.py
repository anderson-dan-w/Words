#!/usr/bin/python3
# python modules
import os
import collections

# dwanderson modules
from dwanderson import texts

words = set()
for fname in (texts):
    _w = str(open(fname, "r").read()).replace("\r","").upper().split("\n")
    words.update(_w)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
primes = [ 2,  3,  5,  7, 11, 13, 17, 19, 23, 29, 31, 37,  41,
          43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
primeabet = collections.defaultdict(int)
primeabet.update(zip(alphabet, primes))

scrabble_scores = collections.defaultdict(int)
scrabble_scores.update(zip(alphabet, [1, 3, 3,  2, 1, 4, 2, 4, 1, 8, 5, 1,  3,
                                     1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]))
scrabble_distr = collections.defaultdict(int)
scrabble_distr.update(zip(alphabet, [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2,
                                    6, 8, 2, 1,  6, 4, 6, 4, 2, 2, 1, 2, 1]))
