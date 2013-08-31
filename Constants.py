#!/usr/bin/python3
# python modules
import os
import collections

py_dir = os.path.realpath(os.path.dirname(__file__)) + "/"
py_text_dir = py_dir + "text/"
TWL06_txt = py_text_dir + "TWL06.txt"
WORDS_txt = py_text_dir + "WORDS.txt"

words = set()
for fname in (TWL06_txt, WORDS_txt):
    _w = str(open(fname, "r").read()).replace("\r","").upper().split("\n")
    words.update(_w)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
primes = [ 2,  3,  5,  7, 11, 13, 17, 19, 23, 29, 31, 37,  41,
          43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
primeabet = collections.defaultdict(int)
primeabet.update(zip(alphabet, primes))

