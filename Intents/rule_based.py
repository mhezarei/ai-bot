import os

import pandas as pd
from hazm import *
from typing import Tuple

unused_chars = ['-', '،', '_', '\n', '//', '/', '\u200c', 'ـ', '?', '؟']
norm = Normalizer()
COMB_SCORE = 3
WORD_SCORE = 1


def get_sw(filename: str) -> list:
	with open(filename, encoding="utf-8") as f:
		sw = f.read().split('\n')
		return sw


def get_list_from(filename: str) -> list:
	with open(filename) as f:
		temp = f.read().split('=')
		ret = []
		for t in temp:
			ret.append([w for w in t.split('\n') if w != ''])
		return ret


def parse_shamsi_events(sw: list) -> Tuple[list, list]:
	events = pd.read_csv("Intents/shamsi_events.csv", encoding="utf-8")
	temp_combs = events["event"].tolist()
	temp_words = []
	for c in temp_combs:
		temp_words += [w for w in norm.normalize(c).split(' ') if w not in sw]
	return list(temp_words), temp_combs


def initialize() -> Tuple[list, list]:
	sw = get_sw("Intents/stop_words_short.txt")
	used_words = get_list_from("Intents/used_words.txt")
	used_combs = get_list_from("Intents/used_combs.txt")
	
	w, c = parse_shamsi_events(sw)
	used_words[3] += w
	used_combs[3] += c
	
	used_words = [list(set(w)) for w in used_words]
	used_combs = [list(set(w)) for w in used_combs]
	
	return used_words, used_combs


words, combs = initialize()


def score(sent: str, c: int) -> int:
	ret = 0
	for comb in combs[c]:
		if comb in sent:
			ret += COMB_SCORE
	for w in words[c]:
		if w in sent.split(' '):
			ret += WORD_SCORE
	return ret


def rule_based_score(sent: str) -> dict:
	sent = norm.normalize(sent)
	scoring = {}
	for i in range(4):
		scoring[i + 1] = score(sent, i)
	return scoring
