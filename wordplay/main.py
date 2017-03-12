import sys
from argparse import ArgumentParser

from wordplay import constants
from wordplay import anagram


def main(sys_args):
    USAGE = "{} <letters> [-n=nwords] [--MIN=minsize]".format(sys.argv[0])
    DESCR = "Returns list of anagrams for given letters and args"
    p = ArgumentParser(usage=USAGE, description=DESCR)
    p.add_argument("letters", type=str, help="letters to anagramize")
    p.add_argument('-n', '--nwords', type=int, default=1,
            help='Number of words to comprise a solution, default=1')
    p.add_argument('--MIN', type=int, default=3,
            help='Minimum number of letters in each anagram, default=3')
    p.add_argument('-e', '--extra', type=int, default=0,
            help="number of extra, 'variable' letters to use, default=0")
    p.add_argument('-s', '--start', type=str, default='A',
            help="Letter to start <--extra> letters at, default='A'")
    p.add_argument('-c', '--condensed', action='store_true',
            help='Prints condensed results in the <--extra> case')
    args = p.parse_args(sys_args)

    ## error-check input
    letters = args.letters.upper()
    nwords, MIN = args.nwords, args.MIN
    extra, start, condensed = args.extra, args.start, args.condensed
    if isinstance(start, str):
        start = constants.ALPHABET.index(start)
    if nwords * MIN > len(letters):
        p.error("nwords * MIN can't be greater than legnth of letters...")
    if any(val < 0 for val in (nwords, MIN, extra, start)):
        p.error("negative values for arguments make no physical sense")

    if extra == 0:
        anagrams = anagram.looping_anagram(letters, nwords, MIN)
        print(anagrams)
    else:
        anagrams = anagram.plus_many(letters, extra, nwords, MIN, start)
        if condensed:
            anagram_set = set()
            for s in anagrams.values():
                anagram_set.update(s)
            print(anagram_set)
        else:
            print(anagrams)

    plural = '' if len(anagrams) == 1 else 's'
    print("Found {} answer{}".format(len(anagrams), plural))
    return

##############################################################################
if __name__ == '__main__':
    main(sys.argv[1:])
