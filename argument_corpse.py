import pandas as pd


with open("stop_words_short.txt", encoding="utf-8") as f:
    sw = f.read().split('\n')


corpse = []
unused_chars = ['-', '،', '_', '\n', '//', '/', 'ـ', '?', '؟', '.', '؛']

with open("used_combs.txt") as f:
    temp = f.read().split('=')
    ret = []
    for t in temp:
        ret.append([w for w in t.split('\n') if w != ''])
    corpse += ret

with open("used_words.txt") as f:
    temp = f.read().split('=')
    ret = []
    for t in temp:
        ret.append([w for w in t.split('\n') if w != '' and w not in sw])
    corpse = corpse + ret

# events
df = pd.read_csv("shamsi_events.csv", encoding="utf-8")
events = list(set(df["event"].tolist()))
clean = []
for e in events:
    s = e
    for c in unused_chars:
        s = s.replace(c, ' ')
    clean.append(s)
clean2 = []
for e in clean:
    clean2 = clean2 + [w for w in e.split(' ') if w != '']
clean2 = list(set(clean2))

# countries
df = pd.read_csv("IP2LOCATION-COUNTRY-MULTILINGUAL.CSV",
                 encoding="utf-8",
                 header=None, skiprows=4981, nrows=249)
countries = df[5].tolist()
new = []
for c in countries:
    new = new + [w for w in c.split(' ') if w != '' and w not in sw]
new = list(set(new))
print(new)

# cities
