from persiantools.jdatetime import JalaliDate
from dateparser.calendars.jalali import JalaliCalendar
import dateparser
import re


def find_dates(sentence_lem):
	en_dates = []
	fa_dates = []
	times = []
	sentence = find_dates_replace(sentence_lem)
	print("--------->", sentence)

	for regX in ["امروز", "دیروز", "فردا",
					r"([\u0660-\u0669]|[\d]+)[\s]روز[\s]پیش", r"([\u0660-\u0669]|[\d]+)[\s]هفته[\s]پیش",
					r"([\u0660-\u0669]|[\d]+)[\s]روز[\s]بعد", r"([\u0660-\u0669]|[\d]+)[\s]هفته[\s]بعد"]:
		if re.search(regX, sentence) is not None:
			en_datetime = dateparser.parse(re.search(regX, sentence).group(0), 
											settings={'TIMEZONE': '+0330'})
			fa_datetime = JalaliDate(en_datetime)
			fa_dates.append(fa_datetime.strftime('%Y-%m-%d'))

	if len(fa_dates) == 0:
		en_datetime = dateparser.parse('امروز',
										settings={'TIMEZONE': '+0330'})
		fa_datetime = JalaliDate(en_datetime)
		fa_dates.append(fa_datetime.strftime('%Y-%m-%d'))

	return fa_dates

def find_dates_replace(sentence):

	sentence = sentence.replace("پس فردا", "2 روز بعد")
	sentence = sentence.replace("پریروز", "2 روز پیش")
	sentence = sentence.replace("هفته بعد", "1 هفته بعد")
	sentence = sentence.replace("هفته پیش", "1 هفته پیش")
	sentence = sentence.replace('ابان', 'آبان')
	sentence = sentence.replace('اذر', 'آذر')

	#replace numbers
	sentence = sentence.replace("یک", "1")
	sentence = sentence.replace("دو", "2")
	sentence = sentence.replace("سه", "3")
	sentence = sentence.replace("چهار", "4")
	sentence = sentence.replace("پنج", "5")
	sentence = sentence.replace("شش", "6")
	sentence = sentence.replace("هفت", "7")
	sentence = sentence.replace("هشت", "8")
	sentence = sentence.replace("نه", "9")
	sentence = sentence.replace("ده", "10")
	sentence = sentence.replace("یازده", "11")
	sentence = sentence.replace("دوازده", "12")
	sentence = sentence.replace("سیزده", "13")
	sentence = sentence.replace("چهارده", "14")
	sentence = sentence.replace("پانزده", "15")
	sentence = sentence.replace("شانزده", "16")
	sentence = sentence.replace("هفده", "17")
	sentence = sentence.replace("هجده", "18")
	sentence = sentence.replace("نوزده", "19")
	sentence = sentence.replace("بیست", "20")
	sentence = sentence.replace("بیست و 1", "21")
	sentence = sentence.replace("بیست و 2", "22")
	sentence = sentence.replace("بیست و 3", "23")
	sentence = sentence.replace("بیست و 4", "24")
	sentence = sentence.replace("بیست و 5", "25")
	sentence = sentence.replace("بیست و 6", "26")
	sentence = sentence.replace("بیست و 7", "27")
	sentence = sentence.replace("بیست و 8", "28")
	sentence = sentence.replace("بیست و 9", "29")
	sentence = sentence.replace("سی", "30")
	sentence = sentence.replace("سی و 1", "31")

	return sentence
