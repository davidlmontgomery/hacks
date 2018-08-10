#!/usr/bin/env python
"""
Generate a random string that is plausibly pronounceable in English.

"""
import random

VOWELS = ('a', 'e', 'i', 'o', 'u',)
CONSONANT_START = {
    'b': ('l', 'r',),
    'c': ('h', 'l', 'r',),
    'd': ('r', 'w',),
    'f': ('l', 'r',),
    'g': ('l', 'r', 'w',),
    'h': (),
    'j': (),
    'k': ('l', 'r',),
    'l': (),
    'm': (),
    'n': (),
    'p': ('l', 'r',),
    'qu': (),
    'r': (),
    's': ('c', 'h', 'hr', 'k', 'kr', 'kw', 'l', 'm', 'n', 'p', 'pl', 'pr', 't', 'tr', 'w',),
    #'sh': ('r',),
    #'sk': ('r', 'w',),
    #'sp': ('l', 'r',),
    #'st': ('r',),
    't': ('h', 'hr', 'r', 'w',),
    #'th': ('r',),
    'v': ('l',),
    'w': (),
    'x': (),
    'y': (),
    'z': (),
}
CONSONANT_END = {
    'b': ('d', 's',),
    'c': ('t',),
    'ch': ('t',),
    'd': ('s',),
    'f': ('s', 't',),
    'g': ('d', 's',),
    'h': (),
    'j': ('d',),
    'k': ('s', 't',),
    'l': ('b', 'ch', 'cht', 'd', 'f', 'j', 'jd', 'k', 'kt', 'm', 'p', 'pt', 's', 't', 'v', 'vd', ),
    #'lj': ('d',),
    #'lk': ('t',),
    #'lp': ('t',),
    #'lv': ('d',),
    #'lch': ('t',),
    'm': ('d', 'f', 'ft', 'p', 'pf', 'pft', 's',),
    #'mf': ('t',),
    #'mp': ('f', 't',),
    'n': ('ch', 'cht', 'd', 'g', 'gd', 'gs', 'j', 'jd', 'k', 's', 't', 'th', 'z',),
    #'ng': ('d', 's',),
    #'nj': ('d',),
    #'nch': ('j', 't',),
    'p': ('s', 't',),
    'r': ('b', 'd', 'k', 'ks', 'l', 'ld', 'm', 'md', 'n', 'nd', 'p', 's', 'st', 't', 'th', 'z',),
    #'rk': ('s',),
    #'rl': ('d',),
    #'rm': ('d',),
    #'rn': ('d',),
    #'rs': ('t',),
    's': ('k', 'p', 't',),
    'sh': ('t',),
    't': ('t',),
    'th': ('d', 's',),
    'v': ('d', 's',),
    'w': (),
    'x': (),
    'y': (),
    'z': ('d', 'h', 'hd'),
    #'zh': ('d',),
}

def main():
    """Print a random plausibly-pronounceable string."""
    start = random.choice(CONSONANT_START.keys())
    more_start = CONSONANT_START[start]
    if more_start:
        start += random.choice(more_start)
    vowel = random.choice(VOWELS)
    end = random.choice(CONSONANT_END.keys())
    more_end = CONSONANT_END[end]
    if more_end and random.random() < 0.20:
        end += random.choice(more_end)
    word = start + vowel + end
    print word

if __name__ == '__main__':
    for __ in range(10):
        main()
