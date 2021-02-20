import numpy as np


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


def correct(word: str) -> dict:
    with open('argument_corpse.txt') as f:
        data = f.read().split('\n')
        data.remove('')
    
    distances = {w: lv(w, word) for w in data}
    return {k: v for k, v in
            sorted(distances.items(), key=lambda item: item[1], reverse=True)}


print(correct("تران"))
