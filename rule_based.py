#!/usr/bin/env python
# coding: utf-8

# In[3]:


get_ipython().run_line_magic('config', 'Completer.use_jedi = False')


# In[4]:


import numpy as np
import pandas as pd
from hazm import *
from collections import Counter
from typing import Tuple


# In[ ]:





# In[5]:


unused_chars = ['-', '،', '_', '\n', '//', '/', '\u200c', 'ـ', '?', '؟']


# In[6]:


norm = Normalizer()


# In[7]:


COMB_SCORE = 6
WORD_SCORE = 2


# In[ ]:





# In[8]:


def get_sw(filename: str) -> list:
    with open(filename, encoding="utf-8") as f:
        sw = f.read().split('\n')
        return sw


# In[9]:


def get_list_from(filename: str) -> list:
    with open(filename) as f:
        temp = f.read().split('=')
        ret = []
        for t in temp:
            ret.append([w for w in t.split('\n') if w != ''])
        return ret


# In[10]:


def parse_shamsi_events(sw: list) -> Tuple[list, list]:
    events = pd.read_csv("shamsi_events.csv", encoding="utf-8")
    combs = events["event"].tolist()
    words = []
    for c in combs:
        words += [w for w in norm.normalize(c).split(' ') if w not in sw]
    return list(words), combs


# In[11]:


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


# In[ ]:





# In[12]:


words, combs = initialize()


# In[ ]:





# In[13]:


def score(sent: str, c: int) -> int:
    ret = 0
    for comb in combs[c]:
        if comb in sent:
            ret += COMB_SCORE
    for w in words[c]:
        if w in sent.split(' '):
            ret += WORD_SCORE
    return ret


# In[23]:


def total_score(sent: str) -> dict:
    scoring = {}
    for i in range(4):
        scoring[i] = score(sent, i)
    return scoring


# In[ ]:





# In[24]:


sent = "فردا هوا ابری است؟"
total_score(norm.normalize(sent))


# In[ ]:




