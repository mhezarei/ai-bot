import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import pandas as pd
from rule_based import rule_based_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, LSTM
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json

mapping = {0: "weather",
           1: "religious time",
           2: "time",
           3: "date",
           4: "unknown"}

df = pd.read_csv("questions and data.csv", index_col=0)
df_x = df["questions"].values
df_y = df["class0"].values
# df = pd.read_csv("mh_clean.csv")
# df_x = df['sentence'].values
# df_y = df['class'].values
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
    model.add(LSTM(150))
    model.add(Dense(5, activation='sigmoid'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=15, verbose=1)
    evaluation = model.evaluate(x_test, y_test, verbose=1)

    return model, evaluation


# model, eval_summary = train_model()
# print(eval_summary)
# model_json = model.to_json()
# with open("all_lstm_model.json", "w") as json_file:
#     json_file.write(model_json)
# model.save_weights("all_lstm_model_weights.h5")
# print("Saved model to disk")

def predict(sent: str) -> int:
    json_file = open('all_lstm_model.json', 'r')

    model = json_file.read()
    json_file.close()
    model = model_from_json(model)
    model.load_weights("all_lstm_model_weights.h5")

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
