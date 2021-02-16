#!/usr/bin/env python
# coding: utf-8

# In[27]:


from hazm import * 


# In[256]:


combs = []
with open("split_combs", "r") as a_file:
    for line in a_file:
        combs.append(line.strip())


# In[257]:


def clean_sent (sent):
    id_g = 1
    dic = {}
    for comb in combs : 
        if comb in sent :
            word = 'کلمه' + str(id_g)
            id_g += 1
            dic[word] = comb
            sent = sent.replace(comb, word)
    return sent, dic


# In[258]:


def find_index (words, word_to_find):
    indexes = []
    for index, word in enumerate(words) : 
        if word.strip() == word_to_find.strip():
            indexes.append(index)
            
    return indexes


# In[259]:


def should_be (indexes, i):
    for index in indexes : 
        if (i == index -1) or (i == index + 1) : 
            return True;
    return False;


# In[260]:


def get_chunks (indexes, words):
    chunks = []
    final = ''
    temp = False
    small_chunk = []
    for i , word in enumerate(words):
        if should_be(indexes, i) == True: 
            if temp == False : 
                small_chunk.append(word)
                temp = True 
            else :
                small_chunk.append(word)
                chunks.append(small_chunk)
                small_chunk = []
                temp = False
        else : 
            if temp == True : 
                final += " + "
            else :
                final += word
                final += " "
    return chunks, final


# In[261]:


def add_one (sent, arg):
    sents = []
    for word in arg :
        sents.append(sent.replace("+", word, 1))
    return sents


# In[262]:


def create_sents (sent, args):
    sents = []
    number = 0 
    res = []
    counter = 0
    for i, arg in enumerate(args) : 
        if i == 0 :
            sents.append(sent)
        else :
            res = []
        for s in sents : 
            res.extend(add_one(s, arg))
        if "+" not in res[0]:
            return res
        
        sents = res
        


# In[263]:


def replace_dic (dic, sents):
    res = []
    for s in sents : 
        for key in dic : 
            s = s.replace(key, dic[key])
        res.append(s)
    return res


# In[264]:


def split (sent, events):
    for event in events : 
        if ' و ' in event : 
            combs.append(event)
    if 'اختلاف' in sent : 
        sents = []
        sents.append(sent)
        return sents
    sent, dic = clean_sent(sent)
    words = word_tokenize(sent)
    indxs = find_index(words, 'و')
    args, sent = get_chunks(indxs, words)
    if "+" not in sent : 
        sents = []
        sents.append(sent)
        return replace_dic(dic, sents)
    sents = create_sents(sent, args)
    return replace_dic(dic, sents)


# In[ ]:





# In[ ]:




