#!/usr/bin/env python3
from __future__ import print_function, division
import os
import collections
import random

import constants
from general import dwanderson

WORDS = dwanderson.readin_words()
WORD_LEN = collections.defaultdict(list)
WLEN_STARTS = collections.defaultdict(lambda:
                            collections.defaultdict(list))
for word in WORDS:
    WORD_LEN[len(word)].append(word)
    WLEN_STARTS[len(word)][word[0]].append(word)

with open(os.path.join(constants.DATA_DIR, "pi_digits.txt")) as fh:
    pi_digits = [int(c) for c in fh.read() if c.isdigit()]

def genAcrosticIndex():
    index = 0
    yield index
    for digit in pi_digits:
        index += digit
        yield index

def isAcrosticable(word, indices):
    for letter, pi_index in zip(word, indices):
        pi_digit = pi_digits[pi_index]
        if pi_digit == 0:
            pi_digit = 10
        #if not any(w.startswith(letter) for w in WORD_LEN[pi_digit]):
        if not WLEN_STARTS[pi_digit][letter]:
            return False
    return True

def genAcrosticWords(down_len, acrostic_gen):
    indices = [next(acrostic_gen) for _ in range(down_len)]
    return [w for w in WORD_LEN[down_len] if isAcrosticable(w, indices)]

def makeAcrostic():
    gen = genAcrosticIndex()
    for digit in pi_digits:
        yield random.choice(genAcrosticWords(digit, gen))

def makeRegular(acrostic):
    acrostic_letters = "".join(acrostic)
    words = []
    gen = genAcrosticIndex()
    pi_indices = [next(gen) for _ in range(len(acrostic_letters))]
    for index in range(pi_indices[-1]+1):
        pi_digit = pi_digits[index]
        if pi_digit == 0:
            pi_digit = 10
        if index in pi_indices:
            starting_letter = acrostic_letters[pi_indices.index(index)]
            possibles = WLEN_STARTS[pi_digit][starting_letter]
            if not possibles:
                print("no len {} start with {} (index {})?"
                        .format(pi_digit, starting_letter, index))
            words.append(random.choice(possibles))
        else:
            words.append(random.choice(WORD_LEN[pi_digit]))
    return words

def printPi(words):
    gen = genAcrosticIndex()
    line_indices = []
    while True:
        n = next(gen)
        if n > len(words):
            break
        line_indices.append(n)
    try:
        for i in range(len(line_indices) - 1):
            if i in line_indices:
                print()
            start, stop = line_indices[i:i+2]
            s = " ".join(words[start:stop]).lower()
            print(s[0].upper() + s[1:]) if s else print("---")
    except Exception as e:
        print ("--- Woops: {}".format(e))
        pass

def makePi(num_acrostic_words=15):
    acro = makeAcrostic()
    acrostic_words = [next(acro) for _ in range(num_acrostic_words)]
    return makeRegular(acrostic_words)
 
