#!/usr/bin/env python
# coding: utf-8

# In[31]:


import numpy as np
import pandas as pd
from rule_based import total_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, Flatten, Dense
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# In[32]:


import warnings
warnings.filterwarnings("ignore")


# In[33]:


mapping = {0: "weather", 
           1: "religious time", 
           2: "time", 
           3: "date", 
           4: "unknown"}


# In[34]:


df = pd.read_csv("mh_clean.csv", index_col=0)


# In[47]:


def train_model (): 
    model = Sequential()
    model.add(Embedding(vocab_size, 100, input_length=maxlen))
    model.add(Conv1D(filters=32, kernel_size=16, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    # model.add(Dense(10, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(5, activation='sigmoid'))
    # print(model.summary())
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    summary = model.fit(Xtrain, y_train, epochs=15, verbose=0)
    eval_summary = model.evaluate(Xtest, y_test, verbose=0)
    
    return model, eval_summary


# In[36]:


x = df["sentence"].values
y = df["class"].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state = 42)


# In[37]:


tokenizer = Tokenizer()
tokenizer.fit_on_texts(x)


# In[38]:


maxlen = max([len(s.split()) for s in x])


# In[42]:


enc_docs = tokenizer.texts_to_sequences(x_train)
Xtrain = pad_sequences(enc_docs, maxlen=maxlen, padding='post')


# In[43]:


enc_docs = tokenizer.texts_to_sequences(x_test)
Xtest = pad_sequences(enc_docs, maxlen=maxlen, padding='post')


# In[44]:


vocab_size = len(tokenizer.word_index) + 1


# In[45]:


model, eval_summary = train_model()


# In[46]:


def predict(sent: str) -> int:
    enc_docs = tokenizer.texts_to_sequences(np.array([sent]))
    s = pad_sequences(enc_docs, maxlen=maxlen, padding='post')
    pred = model.predict(s)
    ind = np.argpartition(pred, -2)[-2:].flatten().tolist()
    ind.reverse()
    
    print(f"The first predicted class: {mapping[ind[0]]}")
    print(f"The second predicted class: {mapping[ind[1]]}")
    
    sc = total_score(sent)
    sc[4] = 0
    print(sc)
    
    if sc[ind[0]] >= 2 and sc[ind[1]] <= 2:
        return mapping[ind[0]]
    elif abs(sc[ind[0]] - sc[ind[1]]) <= 2:
        return mapping[ind[0]]  # CHECK THIS PLEASE
    elif ind[0] == 4 and max(list(sc.values())) <= 2 and sc[ind[1]] != 2:
        return 'unknown'
    # HANDLE NN BEING RIGHT AND RULE-BASED BEING WRONG
    else:
        return mapping[ind[0]]


# In[ ]:




