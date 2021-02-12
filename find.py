from __future__ import unicode_literals
from find_cities import find_cities
from find_dates import find_dates
from find_events import find_events
from find_religious_time import find_religious_time
from find_time import find_date_time
from pipeline_sentence import pipeline_sentence
from tokens_in_sentence import find_tokens_in_sentence
from find_calendar_types import find_calendar_types
from find_weather import find_weather_method


# If you don't have model -> Comment 7, 8, 23, 24 lines and Uncomment 27, 28, 29 lines

def find(sentence_temp, model, tokenizer):
    sentence = sentence_temp
    try:
        calender_types = find_calendar_types(sentence)
    except Exception:
        calender_types = []
    try:
        religious_times = find_religious_time(sentence)
    except Exception:
        religious_times = []
    for religious_time in religious_times:
        sentence = sentence.replace(religious_time, ' ')
    if 'افق' in sentence:
        sentence = sentence.replace('افق', ' ')

    sentence_ner, sentence_ner_lem, sentence_lem, sentence = pipeline_sentence(sentence, model, tokenizer)
    tokens, tokens_lem = find_tokens_in_sentence(sentence_ner,
                                                 sentence_ner_lem)

    try:
        method = find_weather_method(sentence_lem)
    except Exception:
        method = 'cond'

    try:
        cities = find_cities(tokens, sentence)
        for explicit_city in ["اسلام آباد"]:
            if explicit_city in sentence_lem:
                cities.append(explicit_city)
        cities = [city.replace("شهر ", "") for city in cities]
    except Exception:
        # raise ValueError("find_cities Error!")
        cities = []
    # if intent = unknown pass -1 as second arg
    try:
        dates = find_dates(sentence_lem)
    except Exception:
        # raise ValueError("find_dates Error!")
        dates = []
    try:
        times = find_date_time(tokens_lem, sentence)
    except Exception:
        # raise ValueError("find_times Error!")
        times = []

    try:
        events, dates = find_events(sentence_temp, dates)
    except Exception:
        # raise ValueError("find_events_dates Error!")
        events, dates = [], []

    answer = {'type': '', 'city': cities, 'date': dates, 'time': times,
              'religious_time': religious_times,
              'calendar_type': calender_types,
              'event': events, 'api_url': [], 'result': ''}
    return answer, method
