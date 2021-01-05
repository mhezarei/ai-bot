import pandas as pd
import os
from hazm import *
from itertools import groupby
import math

p = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(p, "answers_clean.csv")
answers_clean = pd.read_csv(p, index_col=0)
f = os.path.join(p, "stop_words_short.txt")
text_file = open(f,
                 encoding="utf8")  # I'm not really sure about removing stop words
stop_words = text_file.read().split("\n")


def remove_sw(sent_tokens):
	final_tokens = []
	for token in sent_tokens:
		if token not in stop_words:
			final_tokens.append(token)
	
	return final_tokens


def unique_in_list(tokens):
	unique_list = []
	for x in tokens:
		if x not in unique_list:
			unique_list.append(x)
	return unique_list


def word_tokenizing(remove_stop_word=True):
	sents = answers_clean['sentense']
	all_tokens = []
	max_tokens_per_line = 0
	for sent in sents:
		tokens = word_tokenize(sent)
		if remove_stop_word:
			tokens = remove_sw(tokens)
		if len(tokens) > max_tokens_per_line:
			max_tokens_per_line = len(tokens)
		all_tokens.append(tokens)
	return all_tokens, max_tokens_per_line


def calculate_df(all_tokens):
	DF = {}
	for tokens in all_tokens:
		tokens = unique_in_list(tokens)
		for token in tokens:
			try:
				DF[token] += 1
			except:
				DF[token] = 1
	
	return DF, len(all_tokens)


def calculate_tf_idf(all_tokens, DF, number_of_documents):
	sentenses = []
	for sent_tokens in all_tokens:
		sentense = []
		number_of_tokens = len(sent_tokens)
		tf = dict(zip([key for key, group in groupby(sent_tokens)],
		              [len(list(group)) for key, group in
		               groupby(sent_tokens)]))
		for token in sent_tokens:
			idf = math.log(number_of_documents / DF[token])
			word_tf = tf[token] / number_of_tokens
			sentense.append(word_tf * idf)
		sentenses.append(sentense)
	
	return sentenses


def max_padding(vectors, max_tokens_per_line):
	padded_sentenses = []
	for vector in vectors:
		if len(vector) < max_tokens_per_line:
			pad = max_tokens_per_line - len(vector)
			vector.extend([0] * pad)
			padded_sentenses.append(vector)
		else:
			padded_sentenses.append(vector)
	return padded_sentenses


def main():
	all_tokens, max_tokens_per_line = word_tokenizing()
	DF, number_of_documents = calculate_df(all_tokens)
	vectors = calculate_tf_idf(all_tokens, DF, number_of_documents)
	assert (len(vectors) == len(all_tokens))
	padded = max_padding(vectors, max_tokens_per_line)
	df = pd.DataFrame(padded)
	p = os.path.dirname(os.path.abspath(__file__))
	f = os.path.join(p, "tf_idf_padded.csv")
	df.to_csv(f)


if __name__ == '__main__':
	main()
