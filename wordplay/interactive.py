#!/usr/bin/env python3

## python imports
import collections
import copy
import itertools

## dwanderson imports
import dwanderson

WORDS = dwanderson.readin_words()

@dwanderson.time_me
def unleave(string, MIN=None):
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
    ## get all the unleaves...
    interleaves = []
    for string in strings:
        interleaves.append(unleave(string, MIN, time_me=False))
    ## make sure we got solutions...
    if any(len(interleave) == 0 for interleave in interleaves):
        print("Couldn't find answers for some strings...")
        return interleaves
    ## find longest one, so we know how many columns to read
    ncols = max(len(string) for string in interleaves[0])
    answers = [set([""]) for i in range(ncols)]
    ## for each column...
    for i in range(ncols):
        ## take each unleave in order...
        for interleave in interleaves:
            new_set = set()
            ## take each of that unleave's answers, append the column-letter
            for string in interleave:
                new_set.update([s + string[i] for s in answers[i]])
            answers[i] = new_set
    ## filter out all non-words
    for index, answer in enumerate(answers):
        word_set = set()
        word_set.update([word for word in answer if word in WORDS])
        answers[index] = word_set or None
    return answers
