import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import pandas as pd
from Intents.rule_based import total_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, Flatten, \
	Dense
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


mapping = {0: "weather",
           1: "religious time",
           2: "time",
           3: "date",
           4: "unknown"}

df = pd.read_csv("Intents/mh_clean.csv", index_col=0)
x = df["sentence"].values
y = df["class"].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25,
                                                    random_state=42)
tokenizer = Tokenizer()
tokenizer.fit_on_texts(x)
max_len = max([len(s.split()) for s in x])
enc_docs = tokenizer.texts_to_sequences(x_train)
x_train = pad_sequences(enc_docs, maxlen=max_len, padding='post')
enc_docs = tokenizer.texts_to_sequences(x_test)
x_test = pad_sequences(enc_docs, maxlen=max_len, padding='post')
vocab_size = len(tokenizer.word_index) + 1


def train_model():
	model = Sequential()
	model.add(Embedding(vocab_size, 100, input_length=max_len))
	model.add(Conv1D(filters=32, kernel_size=16, activation='relu'))
	model.add(MaxPooling1D(pool_size=2))
	model.add(Flatten())
	model.add(Dense(10, activation='relu'))
	model.add(Dense(5, activation='sigmoid'))
	model.compile(loss='sparse_categorical_crossentropy', optimizer='adam',
	              metrics=['accuracy'])
	model.fit(x_train, y_train, epochs=15, verbose=0)
	evaluation = model.evaluate(x_test, y_test, verbose=0)
	
	return model, evaluation


model, eval_summary = train_model()


def predict(sent: str) -> int:
	enc = tokenizer.texts_to_sequences(np.array([sent]))
	s = pad_sequences(enc, maxlen=max_len, padding='post')
	pred = model.predict(s)
	ind = np.argpartition(pred, -2)[-2:].flatten().tolist()
	ind.reverse()
	
	sc = total_score(sent)
	sc[4] = 0
	
	if sc[ind[0]] >= 2 and sc[ind[1]] <= 2:
		return ind[0] + 1 if ind[0] != 4 else -1
	elif abs(sc[ind[0]] - sc[ind[1]]) <= 2:
		return ind[0] + 1 if ind[0] != 4 else -1  # CHECK THIS PLEASE
	elif ind[0] == 4 and max(list(sc.values())) <= 2 and sc[ind[1]] != 2:
		return -1
	# HANDLE NN BEING RIGHT AND RULE-BASED BEING WRONG
	else:
		return ind[0] + 1 if ind[0] != 4 else -1
