#!/usr/bin/python3

## python imports
import collections
import itertools

## dwanderson imports
import dwanderson

WORDS = dwanderson.readin_words()

@dwanderson.time_me
def interleave(string, MIN=None):
    string = string.upper().replace(" ","")
    nletts = len(string)
    if MIN is None:
        MIN = nletts // 2
    answers = set()
    max_iters = 2 ** (nletts - 1)
    for itr in range(max_iters):
        string1 = ""
        string2 = ""
        for idx, lett in enumerate(string):
            if (2 ** idx) & itr:
                string1 += lett
            else:
                string2 += lett
        if len(string1) < MIN or len(string2) < MIN:
            continue
        if string1 in WORDS and string2 in WORDS:
            answers.add(string1 + " " + string2)
    return answers

@dwanderson.time_me
def group_unleave(strings, MIN=None):
    answers = []
    for string in strings:
        answers.append(interleave(string, MIN, time_me=False))
    if any(len(answer) == 0 for answer in answers):
        print("Couldn't find answers for some strings...")
        return answers
    ## this is proving a little tricky to remember how to do
    return answers
