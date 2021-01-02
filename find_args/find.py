from __future__ import unicode_literals
from find_args.find_cities import find_cities
from find_args.find_dates import find_dates
from find_args.find_events import find_events
from find_args.find_religious_time import find_religious_time
from find_args.find_time import find_date_time
from find_args.pipeline_sentence import pipeline_sentence
from find_args.tokens_in_sentence import find_tokens_in_sentence
from find_args.find_calendar_types import find_calendar_types
from find_args.find_weather import find_weather_method


def find(sentence_temp):
	sentence = sentence_temp
	calender_types = find_calendar_types(sentence)
	religious_times = find_religious_time(sentence)
	for religious_time in religious_times:
		sentence = sentence.replace(religious_time, ' ')
	if 'افق' in sentence:
		sentence = sentence.replace('افق', ' ')

	sentence_ner, sentence_ner_lem, sentence_lem= pipeline_sentence(sentence)
	tokens, tokens_lem = find_tokens_in_sentence(sentence_ner,
	                                             sentence_ner_lem)

	# sentence_lem = "فردا هوا تهران ابر #است ؟"
	# tokens, tokens_lem = ([{'word': 'فردا', 'entity_group': 'date', 'index': 1}, {'word': 'تهران', 'entity_group': 'location', 'index': 3}], 
	# 				[{'word': 'فردا', 'entity_group': 'date', 'index': 1}, {'word': 'تهران', 'entity_group': 'location', 'index': 3}])
	# tokens, tokens_lem = (
	# 	[{'entity_group': 'organization', 'index': 3, 'word': 'جمهوری اسلامی'},
	# 	 {'entity_group': 'date', 'index': 6, 'word': 'سال ۱۴۰۰'}],
	# 	[{'entity_group': 'date', 'index': 6, 'word': 'سال ۱۴۰۰'}])
	
	method = find_weather_method(sentence_lem)

	cities = find_cities(tokens)
	# if intent = unknown pass -1 as second arg
	dates = find_dates(tokens_lem)
	times = find_date_time(tokens_lem, sentence)
	
	events, dates = find_events(sentence, dates)
	
	answer = {'type': '', 'city': cities, 'date': dates, 'time': times,
	          'religious_time': religious_times,
	          'calendar_type': calender_types,
	          'event': events, 'api_url': [], 'result': ''}
	return answer, method
