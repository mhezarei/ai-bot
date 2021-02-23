#!/usr/bin/env python
# coding: utf-8

# In[1]:


from hazm import * 


# In[2]:


combs = []
with open("split_combs", "r") as a_file:
    for line in a_file:
        combs.append(line.strip())


# In[3]:


def clean_sent (sent, combs, id_g = 1):
    dic = {}
    for comb in combs : 
        if comb in sent :
            word = 'کلمه' + str(id_g)
            id_g += 1
            dic[word] = comb
            sent = sent.replace(comb, word)
    return sent, dic


# In[4]:


def find_index (words, word_to_find):
    indexes = []
    for index, word in enumerate(words) : 
        if word.strip() == word_to_find.strip() and words[index + 1] != 'مناسبت':
            indexes.append(index)
            
    return indexes


# In[5]:


def should_be (indexes, i, r):
    for index in indexes : 
        if (i >= index -r) and (i <= index + r) and i!= index: 
            return True;
    return False;


# In[6]:


def get_chunks (indexes, words):
    chunks = []
    final = ''
    temp = False
    small_chunk = []
    for i , word in enumerate(words):
        if should_be(indexes, i, 1) == True: 
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


# In[7]:


def add_one (sent, arg):
    sents = []
    for word in arg :
        sents.append(sent.replace("+", word, 1))
    return sents


# In[8]:


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
        


# In[9]:


def replace_dic (dic, sents):
    res = []
    for s in sents : 
        for key in dic : 
            s = s.replace(key, dic[key])
        res.append(s)
    return res


# In[10]:


def find_comb_indexes (sent): 
    words = word_tokenize(sent)
    comb_indexes = []
    for i, word in enumerate(words) : 
        if word.startswith('کلمه'): 
            comb_indexes.append(i)
            
    return comb_indexes


# In[11]:


def append(words):
    res = ""
    for w in words :
        res += w 
        if w != 'کلمه' :
            res += " "
    return res


# In[12]:


def first_split(comb_indexes, words):
    last = 0
    final = []
    for i in comb_indexes: 
        if i - last == 3 : 
            return split_medium(words)
        elif i - last > 3 :
            final.append(append(words[last:i-1]))
            last = i
    final.append(append(words[last:]))
    
    return final


# In[13]:


def split_near (sent):
    words = word_tokenize(sent)
    indxs = find_index(words, 'و')
    args, sent = get_chunks(indxs, words)
    if "+" not in sent : 
        sents = []
        sents.append(sent)
        return replace_dic(dic, sents)
    sents = create_sents(sent, args)
    return sents


# In[14]:


def complete_split (firsts):
    final = []
    for s in firsts : 
        if ' و ' in s : 
            final.extend(split_near(s))
        else :
            final.append(s)
    return final


# In[15]:


def make_sent(sent, args):
    final = []
    for arg in args : 
        final.append(sent.replace("+", arg, 1))
    return final


# In[16]:


def get_chunks_medium (indexes, words, r):
    chunks = []
    final = ''
    temp = False
    small_chunk = []
    for i , word in enumerate(words):
        if should_be(indexes, i, r) == True: 
            small_chunk.append(word)
        else : 
            if word.strip() == 'و' and i in indexes  : 
                i_ind = indexes.index(i)
                if indexes[i_ind - 1] == i - 3 : 
                    final += ""
                else :
                    final += " + "
                chunks.append(small_chunk)
                small_chunk = []
            else :
                final += word
                final += " "
    chunks.append(small_chunk)
    return chunks, final


# In[17]:


def split_medium(words):
    indxs = find_index(words, ' و ')
    chunks, sent = get_chunks_medium(indxs, words, 2)
    counter = 0
    final_chunks = []
    s = ''
    anws = []
    for chunk in chunks : 
        for w in chunk :
            s += w 
            s += ' '
            counter += 1
            if counter == 2 : 
                counter = 0 
                final_chunks.append(s)
                s = ''
    sents = sent.split(' و ')
    for s in sents : 
        if ' و ' not in s : 
            anws.append(s)

    return make_sent(sent, final_chunks)


# In[18]:


def split(sent, events): 
    if 'اختلاف' in sent or 'تفاوت' in sent: 
        sents = []
        sents.append(sent)
        return sents
    if ' و ' not in sent : 
        return [sent]
    sent , dic = clean_sent(sent, combs)
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





# In[ ]:





# In[ ]:





# In[ ]:




