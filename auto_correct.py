import numpy as np
from hazm import *

pronunciations = [
    ['ب', 'پ', 'ت', 'د', 'ط'], ['گ', 'ق', 'غ', 'ف', 'ک'],
    ['ز', 'ذ', 'ض', 'ٰژ'], ['ث', 'س', 'ص'], ['ج', 'چ'], ['ح', 'ه'], ['ا', 'ع'],
]
MAX_DIFF = 10


def close_pronunciation(letter: str) -> list:
    for lst in pronunciations:
        if letter in lst:
            return lst
    return []


def lv(s, t):
    rows = len(s) + 1
    cols = len(t) + 1
    r, c = 0, 0
    distance = np.zeros((rows, cols), dtype=int)

    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k

    for col in range(1, cols):
        for row in range(1, rows):
            r, c = row, col
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = 1
            distance[row][col] = min(distance[row - 1][col] + 1,
                                     distance[row][col - 1] + 1,
                                     distance[row - 1][col - 1] + cost)

    return distance[r][c]


def correct(word: str) -> str:
    with open('argument_corpse.txt') as f:
        data = f.read().split('\n')
        data.remove('')

    distances = {w: lv(w, word) for w in data}
    res = {k: v for k, v in
           sorted(distances.items(), key=lambda item: item[1], reverse=True)}
    for r in res.keys():
        if res[r] == 0:
            return r
    for i in range(1, MAX_DIFF):
        close_words = [w for w, v in res.items() if v == i and len(word) == len(w)]
        if len(close_words) == 1:
            return close_words[0]
        else:
            for w in close_words:
                diff_letter = [(i, c) for i, c in enumerate(w) if c != word[i]][0]
                close_p = close_pronunciation(diff_letter[1])
                if close_p and word[diff_letter[0]] in close_p:
                    return w


def auto_correct(sentence: str):
    symbols = "!\"#$%&()*+-./;<=>?@[\\]^_`{|}~\n،,؟؛"
    for i in symbols:
        sentence = str.replace(sentence, i, ' ')
    words = word_tokenize(sentence)
    new_sen = ""
    for i in range(len(words) - 1):
        words[i] = correct(words[i])
        new_sen = new_sen + " " + words[i]
    new_sen = new_sen + " " + words[-1]
    return new_sen
