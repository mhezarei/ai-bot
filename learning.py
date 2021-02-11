import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import pandas as pd
from rule_based import rule_based_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, Flatten, \
	Dense, BatchNormalization
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json

mapping = {0: "weather",
           1: "religious time",
           2: "time",
           3: "date",
           4: "unknown"}


p = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(p, "mh_clean.csv")

df = pd.read_csv(f, index_col=0)
df_x = df["sentence"].values
df_y = df["class"].values
x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.25,
                                                    random_state=42)
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df_x)
max_len = max([len(s.split()) for s in df_x])
enc_docs = tokenizer.texts_to_sequences(x_train)
x_train = pad_sequences(enc_docs, maxlen=max_len, padding='post')
enc_docs = tokenizer.texts_to_sequences(x_test)
x_test = pad_sequences(enc_docs, maxlen=max_len, padding='post')
vocab_size = len(tokenizer.word_index) + 1


def train_model():
	model = Sequential()
	model.add(Embedding(vocab_size, 100, input_length=max_len))
	model.add(Conv1D(filters=32,
					 kernel_size=16,
					 activation='relu'))
	model.add(MaxPooling1D(pool_size=2))
	model.add(Flatten())
	model.add(BatchNormalization())
	# model.add(Dense(32, activation='relu'))
	model.add(Dense(16, activation='sigmoid'))
	model.add(Dense(8, activation='sigmoid'))
	model.compile(loss='sparse_categorical_crossentropy', optimizer='adam',
	              metrics=['accuracy'])
	model.fit(x_train, y_train, epochs=15, verbose=0)
	evaluation = model.evaluate(x_test, y_test, verbose=0)
	
	return model, evaluation


# model, eval_summary = train_model()
# model_json = model.to_json()
# with open("model.json", "w") as json_file:
#     json_file.write(model_json)
# print(eval_summary)
# model.save_weights("model.h5")
# print("model saved")

def predict(sent: str) -> int:
	p = os.path.dirname(os.path.abspath(__file__))
	f = os.path.join(p, "model.json")
	json_file = open(f, 'r')
	model = json_file.read()
	json_file.close()
	model = model_from_json(model)
	# load weights into new model
	f = os.path.join(p, "model.h5")
	model.load_weights(f)
	unk = 5
	enc = tokenizer.texts_to_sequences(np.array([sent]))
	s = pad_sequences(enc, maxlen=max_len, padding='post')
	rank = model.predict(s).flatten()
	rank = (np.argpartition(rank, -2)[-2:])[::-1]
	# +1 since the indices are 0-based but the classes are 1-based
	first, second = rank[0] + 1, rank[1] + 1

	rb_score = rule_based_score(sent)
	rb_score[unk] = 0
	# rule-based score of the predicted classes
	x, y = rb_score[first], rb_score[second]

	if max(list(rb_score.keys())) > 50:
		return 4
	
	if first != unk and second != unk:
		if y - x >= 2:
			return second
		else:
			return first
	elif first != unk and second == unk:
		if x >= 1:
			return first
		else:
			s = max(rb_score, key=rb_score.get)
			if s != first and rb_score[s] >= 1:
				return s
			else:
				return -1
	elif first == unk and second != unk:
		if y >= 1:
			return second
		else:
			s = max(rb_score, key=rb_score.get)
			if s != second and rb_score[s] >= 1:
				return s
			else:
				return -1
