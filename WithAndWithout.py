#!/usr/bin.python3

##dwanderson imports
import dwanderson

WORDS = dwanderson.readin_words()

@dwanderson.time_me
def with_and_without(letters, pos=None, MIN=0, MAX=100):
    letters = "".join(l.upper() for l in letters if l.isalpha())
    answers = set()
    for word in WORDS:
        if letters not in word or not (MIN <= len(word) <= MAX):
            continue
        index = word.find(letters)
        if pos is not None and pos != index:
            continue
        without = word[:index] + word[index + len(letters):]
        if without in WORDS:
            answers.add((word, without))
    return answers


##############################################################################

