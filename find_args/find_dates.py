from persiantools.jdatetime import JalaliDate
from dateparser.calendars.jalali import JalaliCalendar
import dateparser
import re


def find_dates(tokens_lem, intent=1):
	en_dates = []
	fa_dates = []
	times = []
	for token in tokens_lem:
		if token['entity_group'] == 'date':
			try:
				regexp = re.compile('۱[۳|۴][--۹][--۹]')
				if regexp.search(token['word']):
					raise (ValueError('a shamsi date'))
				en_datetime = dateparser.parse(token['word'],
				                               settings={'TIMEZONE': '+0330'})
				fa_datetime = JalaliDate(en_datetime)
				fa_dates.append(fa_datetime.strftime('%Y-%m-%d'))
			except:
				try:
					word = token['word']
					word = word.replace('ابان', 'آبان')
					word = word.replace('اذر', 'آذر')
					en_datetime = JalaliCalendar(word).get_date()
					fa_datetime = JalaliDate(en_datetime.date_obj)
					fa_dates.append(fa_datetime.strftime('%Y-%m-%d'))
				except:
					print('error in date')
		if intent != -1 and len(fa_dates) == 0:
			en_datetime = dateparser.parse('امروز',
			                               settings={'TIMEZONE': '+0330'})
			fa_datetime = JalaliDate(en_datetime)
			fa_dates.append(fa_datetime.strftime('%Y-%m-%d'))
	return fa_dates
