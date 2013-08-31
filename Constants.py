#!/usr/bin/python3
# python modules
import os
import collections

py_dir = os.path.realpath(os.path.dirname(__file__)) + "/"
py_text_dir = py_dir + "text/"
TWL06_txt = py_text_dir + "TWL06.txt"
WORDS_txt = py_text_dir + "WORDS.txt"

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
primes = [ 2,  3,  5,  7, 11, 13, 17, 19, 23, 29, 31, 37,  41,
          43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
primeabet = collections.defaultdict(int)
primeabet.update(zip(alphabet, primes))

