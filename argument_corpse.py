import pandas as pd


with open("stop_words_short.txt", encoding="utf-8") as f:
    sw = f.read().split('\n')


corpse = []
unused_chars = ['-', '،', '_', '\n', '//', '/', 'ـ', '?', '؟', '.', '؛']

with open("used_combs.txt") as f:
    temp = f.read().split('=')
    ret = []
    for t in temp:
        h = [w for w in t.split('\n') if w != '']
        for w in h:
            ret += [s for s in w.split(' ') if s != '' and s not in sw]
    corpse += ret

with open("used_words.txt") as f:
    temp = f.read().split('=')
    ret = []
    for t in temp:
        ret += [w for w in t.split('\n') if w != '' and w not in sw]
    corpse += ret

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
corpse += clean2

# countries
df = pd.read_csv("IP2LOCATION-COUNTRY-MULTILINGUAL.CSV",
                 encoding="utf-8",
                 header=None, skiprows=4981, nrows=249)
countries = df[5].tolist()
new = []
for c in countries:
    new = new + [w for w in c.split(' ') if w != '' and w not in sw]
new = list(set(new))
corpse += new

# cities
# df = pd.read_csv("cities15000.txt", sep='\t',
#                  encoding="utf-8", header=None)
# cities = df[3].tolist()
# new2 = []
# for c in cities:
#     new2 = new2 + [w for w in c.split(' ') if w != '' and w not in sw]
# new2 = list(set(new2))
# print(new2)

# questions
df = pd.read_csv("Intents_questions.csv", encoding="utf-8")
questions = df["questions"].tolist()
new = []
for q in questions:
    temp = q
    for c in unused_chars:
        temp = temp.replace(c, ' ')
    new += [w for w in temp.split(' ') if w != '' and w not in sw]
new = list(set(new))
corpse += new


# PLEASE DO NOT RUN THIS AS IT WILL APPEND THE DATA TO THE CORPSE FILE
# corpse = list(set(corpse))
# with open("argument_corpse.txt", "a+") as f:
#     for w in corpse:
#         f.write(w + '\n')
