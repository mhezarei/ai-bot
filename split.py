#!/usr/bin/env python
# coding: utf-8

# In[528]:


from hazm import *

# In[529]:


combs = []
with open("split_combs", "r") as a_file:
    for line in a_file:
        combs.append(line.strip())


# In[530]:


def clean_sent(sent, combs, id_g=1):
    dic = {}
    for comb in combs:
        if comb in sent:
            word = 'کلمه' + str(id_g)
            id_g += 1
            dic[word] = comb
            sent = sent.replace(comb, word)
    return sent, dic


# In[531]:


def find_index(words, word_to_find):
    indexes = []
    for index, word in enumerate(words):
        if word.strip() == word_to_find.strip():
            indexes.append(index)

    return indexes


# In[532]:


def should_be(indexes, i):
    for index in indexes:
        if (i == index - 1) or (i == index + 1):
            return True;
    return False;


# In[533]:


def get_chunks(indexes, words):
    chunks = []
    final = ''
    temp = False
    small_chunk = []
    for i, word in enumerate(words):
        if should_be(indexes, i) == True:
            if temp == False:
                small_chunk.append(word)
                temp = True
            else:
                small_chunk.append(word)
                chunks.append(small_chunk)
                small_chunk = []
                temp = False
        else:
            if temp == True:
                final += " + "
            else:
                final += word
                final += " "
    return chunks, final


# In[534]:


def add_one(sent, arg):
    sents = []
    for word in arg:
        sents.append(sent.replace("+", word, 1))
    return sents


# In[535]:


def create_sents(sent, args):
    sents = []
    number = 0
    res = []
    counter = 0
    for i, arg in enumerate(args):
        if i == 0:
            sents.append(sent)
        else:
            res = []
        for s in sents:
            res.extend(add_one(s, arg))
        if "+" not in res[0]:
            return res

        sents = res


# In[536]:


def replace_dic(dic, sents):
    res = []
    for s in sents:
        for key in dic:
            s = s.replace(key, dic[key])
        res.append(s)
    return res


# In[537]:


def split_near(sent):
    words = word_tokenize(sent)
    indxs = find_index(words, 'و')
    args, sent = get_chunks(indxs, words)
    if "+" not in sent:
        sents = []
        sents.append(sent)
        return replace_dic(dic, sents)
    sents = create_sents(sent, args)
    return sents


# In[538]:


def find_comb_indexes(sent):
    words = word_tokenize(sent)
    comb_indexes = []
    for i, word in enumerate(words):
        if word.startswith('کلمه'):
            comb_indexes.append(i)

    return comb_indexes


# In[539]:


def append(words):
    res = ""
    for w in words:
        res += w
        if w != 'کلمه':
            res += " "
    return res


# In[540]:


def first_split(comb_indexes, words):
    last = 0
    final = []
    for i in comb_indexes:
        if i - last >= 3:
            final.append(append(words[last:i - 1]))
            last = i
    final.append(append(words[last:]))

    return final


# In[541]:


def complete_split(firsts):
    final = []
    for s in firsts:
        if ' و ' in s:
            final.extend(split_near(s))
        else:
            final.append(s)
    return final


# In[542]:


def split(sent, events):
    if 'اختلاف' in sent or 'تفاوت' in sent:
        sents = []
        sents.append(sent)
        return sents
    sent, dic = clean_sent(sent, combs)
    comb_indexes = find_comb_indexes(sent)
    sent, event_dic = clean_sent(sent, events, 60)
    dic.update(event_dic)
    words = word_tokenize(sent)
    firsts = first_split(comb_indexes, words)
    sents = complete_split(firsts)
    return replace_dic(dic, sents)

# In[ ]:


# In[ ]:


# In[ ]:


# In[333]:


# In[334]:


# In[338]:


# In[356]:


# In[372]:


# In[ ]:


# In[ ]:
