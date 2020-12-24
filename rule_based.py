import numpy as np
import pandas as pd
from hazm import *
from collections import Counter

from typing import Tuple
get_ipython().run_line_magic('config', 'Completer.use_jedi = False')
df = pd.read_csv("base_responses.csv", encoding="utf-8").dropna()
df.head()

unused_chars = ['-', '،', '_', '\n', '//', '/', '\u200c', 'ـ', '?', '؟']
COMB_SCORE = 6
WORD_SCORE = 2
norm = Normalizer()

def get_sw(filename: str) -> list:
    with open(filename, encoding="utf-8") as f:
        sw = f.read().split('\n')
        return sw

def get_list_from(filename: str) -> list:
    with open(filename) as f:
        temp = f.read().split('=')
        ret = []
        for t in temp:
            ret.append([w for w in t.split('\n') if w != ''])
        return ret

def parse_shamsi_events(sw: list) -> Tuple[list, list]:
    events = pd.read_csv("shamsi_events.csv", encoding="utf-8")
    combs = events["event"].tolist()
    words = []
    for c in combs:
        words += [w for w in norm.normalize(c).split(' ') if w not in sw]
    return list(words), combs

def initialize() -> Tuple[list, list]:
    sw = get_sw("stop_words_short.txt")
    used_words = get_list_from("used_words.txt")
    used_combs = get_list_from("used_combs.txt")
    
    w, c = parse_shamsi_events(sw)
    used_words[3] += w
    used_combs[3] += c
    
    used_words = [list(set(w)) for w in used_words]
    used_combs = [list(set(w)) for w in used_combs]
    
    return used_words, used_combs

words, combs = initialize()
def score(sent: str, c: int) -> int:
    ret = 0
    for comb in combs[c]:
        if comb in sent:
            print('a', comb)
            ret += COMB_SCORE
    for w in words[c]:
        if w in sent.split(' '):
            print(w, c)
            ret += WORD_SCORE
    return ret

def total_score(sent: str, c: int) -> dict:
    scoring = {}
    for i in range(4):
        scoring[i] = score(sent, i)
    return scoring

def return_scores (sent) :
    c = -1
    print(norm.normalize(sent))
    return total_score(norm.normalize(sent), c)



