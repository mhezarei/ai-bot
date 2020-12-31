import re
import dateparser
from persiantools.jdatetime import JalaliDate
from dateparser.calendars.jalali import JalaliCalendar


def find_date_time(tokens_lem):
	"""
	Calculate time of given string by persian sentences in it and convert
	it to HH:MM :
	  input : string from entity_group 'I_TIM' from tokens_lem
	  output: string
	----------------------------------------
	Function Description:
	  'بعد از ظهر' : Convert to pm (+12h)
	  'نیم'       : Add 30 minutes(+30m)
	  'ربع'       : Add 15 minutes(+15m)
	Assuming that we don't have sentences like this:
	  'شش و ربع کم' : Corresponds to '5:45'
	"""
	# Convert persian number word to digit
	times = []
	for token in tokens_lem:
		string = token['word']
		if token['entity_group'] == 'time':
			try:
				regexp = re.compile('۱[۳|۴][--۹][--۹]')
				if regexp.search(token['word']):
					raise (ValueError('a shamsi time'))
				en_datetime = dateparser.parse(token['word'],
				                               settings={'TIMEZONE': '+0330'})
				fa_datetime = JalaliDate(en_datetime)
				times.append(fa_datetime.strftime('%H-%M'))
			except:
				string = string.replace("یک", "1")
				string = string.replace("دو", "2")
				string = string.replace("سه", "3")
				string = string.replace("چهار", "4")
				string = string.replace("پنج", "5")
				string = string.replace("شش", "6")
				string = string.replace("هفت", "7")
				string = string.replace("هشت", "8")
				string = string.replace("نه", "9")
				string = string.replace("ده", "10")
				string = string.replace("یازده", "11")
				string = string.replace("دوازده", "12")
				# Converting to HH:MM format
				numbers = re.findall(r'\d+', string)
				raw_hour = numbers[0]
				raw_minutes = numbers[1] if len(numbers) == 2 else '0'
				if "بعد از ظهر" in string:
					if int(raw_hour) < 12:
						raw_hour = str(int(raw_hour) + 12)
				if "و نیم" in string:
					raw_minutes = '30'
				elif "و ربع" in string:
					raw_minutes = '15'
				times.append(raw_hour + ':' + raw_minutes.zfill(2))
	
	return times
