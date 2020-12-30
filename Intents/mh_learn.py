#!/usr/bin/env python
# coding: utf-8

# In[36]:


import numpy as np
import pandas as pd
from Intents.rule_based import total_score


# In[37]:


mapping = {0: "weather", 
           1: "religious time", 
           2: "time", 
           3: "date", 
           4: "unknown"}


# In[38]:


df = pd.read_csv("mh_clean.csv", index_col=0)
df


# In[39]:


from sklearn.model_selection import train_test_split

x = df["sentence"].values
y = df["class"].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state = 42)


# In[40]:


from keras.preprocessing.text import Tokenizer

tokenizer = Tokenizer()
tokenizer.fit_on_texts(x)


# In[41]:


maxlen = max([len(s.split()) for s in x])


# In[42]:


from tensorflow.keras.preprocessing.sequence import pad_sequences

enc_docs = tokenizer.texts_to_sequences(x_train)
Xtrain = pad_sequences(enc_docs, maxlen=maxlen, padding='post')


# In[43]:


enc_docs = tokenizer.texts_to_sequences(x_test)
Xtest = pad_sequences(enc_docs, maxlen=maxlen, padding='post')


# In[44]:


vocab_size = len(tokenizer.word_index) + 1


# In[45]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, Flatten, Dense

model = Sequential()
model.add(Embedding(vocab_size, 100, input_length=maxlen))
model.add(Conv1D(filters=32, kernel_size=16, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
# model.add(Dense(10, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(5, activation='sigmoid'))
print(model.summary())


# In[46]:


model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(Xtrain, y_train, epochs=15)


# In[47]:


model.evaluate(Xtest, y_test)


# In[54]:


## saving model
model.save('.')


# In[56]:


## loading the model 
import keras
model = keras.models.load_model('.')


# In[57]:


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


# In[58]:


sent = 'امروز چه مناسبی داریم؟'


# In[59]:


predict(sent)


# In[18]:


from sklearn.feature_extraction.text import CountVectorizer

vec = CountVectorizer()
vec.fit(x_train)
x_train = vec.transform(x_train)
x_test = vec.transform(x_test)


# In[19]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

model = Sequential()
model.add(Dense(64, input_dim=x_train.shape[1], activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(5, activation='sigmoid'))
model.compile(loss="sparse_categorical_crossentropy",
              optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=16, epochs=15)


# In[20]:


score = model.evaluate(x_test, y_test)


# In[21]:


from sklearn.feature_extraction.text import CountVectorizer

sent = np.array(["امروز چه مناسبی داریم؟"])
vec = CountVectorizer()
vec.fit(sent)
sent = vec.transform(sent)


# In[22]:


sent


# In[23]:


model.predict(x_test)


# In[24]:


from sklearn.model_selection import train_test_split

x = df["sentence"].values
y = df["class"].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state = 42)


# In[25]:


from sklearn.feature_extraction.text import TfidfVectorizer

vec = TfidfVectorizer()
vec.fit(x_train)
x_train = vec.transform(x_train)
x_test = vec.transform(x_test)


# In[31]:


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

lr = LogisticRegression()
lr.fit(x_train, y_train)
accuracy_score(y_test, lr.predict(x_test))


# In[ ]:




