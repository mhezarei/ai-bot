import os

import pandas as pd
from hazm import *
from typing import Tuple

unused_chars = ['-', '،', '_', '\n', '//', '/', '\u200c', 'ـ', '?', '؟']
norm = Normalizer()
COMB_SCORE = 3
WORD_SCORE = 1

p = os.path.dirname(os.path.abspath(__file__))


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


def parse_shamsi_events() -> list:
	# this is only needed for date category so we can
	# only check the whole combination and not the words
	f = os.path.join(p, 'shamsi_events.csv')
	events = pd.read_csv(f, encoding="utf-8")
	temp_combs = events["event"].tolist()
	return list(set(temp_combs))


def initialize() -> Tuple[list, list]:
	used_words = get_list_from(os.path.join(p, 'used_words.txt'))
	used_combs = get_list_from(os.path.join(p, 'used_combs.txt'))
	
	c = parse_shamsi_events()
	used_combs[3] += c
	
	used_words = [list(set(w)) for w in used_words]
	used_combs = [list(set(w)) for w in used_combs]
	
	return used_words, used_combs


words, combs = initialize()


def score(sent: str, c: int) -> int:
	ret = 0
	if c == 2:
		if ('ساعت' in sent) and ('چند است' in sent):
			ret += COMB_SCORE
	for comb in combs[c]:
		if comb in sent:
			if c != 3:
				ret += COMB_SCORE
			else:
				ret += 50
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

