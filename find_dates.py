from persiantools.jdatetime import JalaliDate
from dateparser.calendars.jalali import JalaliCalendar
from unidecode import unidecode
import dateparser
import re
import jdatetime


def find_dates(sentence_lem):
    fa_dates = []
    sentence = find_dates_replace(sentence_lem)
    for regX in ["امروز", "دیروز", "فردا", "پارسال", "امسال",
                 r"([\u0660-\u0669]|[\d])+[\s]روز[\s]پیش", r"([\u0660-\u0669]|[\d])+[\s]هفته[\s]پیش",
                 r"([\u0660-\u0669]|[\d])+[\s]سال[\s]پیش",
                 r"([\u0660-\u0669]|[\d])+[\s]روز[\s]بعد", r"([\u0660-\u0669]|[\d])+[\s]هفته[\s]بعد",
                 r"([\u0660-\u0669]|[\d])+[\s]سال[\s]بعد"]:
        en_datetimes = [x.group() for x in re.finditer(regX, sentence)]

        # if re.search(regX, sentence) is not None:
        #     en_datetime = dateparser.parse(re.search(regX, sentence).group(0),
        #                                    settings={'TIMEZONE': '+0330'})
        for strDate in en_datetimes:
            en_datetime = dateparser.parse(strDate, settings={'TIMEZONE': '+0330'})
            fa_datetime = JalaliDate(en_datetime)
            fa_dates.append(fa_datetime.strftime('%Y-%m-%d'))

    # find dates like "18 اسفند"
    dates = [x.group() for x in re.finditer(r"\d+[\s][\u0600-\u06FF]+", sentence)]
    for i in range(len(dates)):
        for per_month in ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'ابان', 'اذر', 'دی', 'بهمن',
                          'اسفند']:
            if per_month in dates[i]:
                en_datetime = JalaliCalendar(dates[i]).get_date()
                fa_datetime = JalaliDate(en_datetime.date_obj)
                temp = fa_datetime.strftime('%Y-%m-%d')

                year = fa_dates[i].split("-")[0]
                month = temp.split("-")[1]
                day = temp.split("-")[2]

                fa_dates[i] = f"{year}-{month}-{day}"
    if len(fa_dates) == 0:
        en_datetime = dateparser.parse('امروز',
                                       settings={'TIMEZONE': '+0330'})
        fa_datetime = JalaliDate(en_datetime)
        fa_dates.append(fa_datetime.strftime('%Y-%m-%d'))
    # find dates like "سال 99", "سال 1399"
    dates = [x.group() for x in re.finditer(r"((سال)|(کدام روز))[\s]\d+", sentence)]
    for i in range(len(dates)):

        splited = dates[i].split(" ")
        year = splited[len(splited) - 1]

        if len(year) == 2:
            year = '13' + year

        year = unidecode(year)

        month = fa_dates[i].split("-")[1]
        day = fa_dates[i].split("-")[2]

        fa_dates[i] = f"{year}-{month}-{day}"

    print("dates : " + str(fa_dates))
    return fa_dates


def find_dates_replace(sentence):
    sentence = sentence.replace('ابان', 'آبان')
    sentence = sentence.replace('اذر', 'آذر')
    sentence = sentence.replace('دیگر', 'بعد')
    sentence = sentence.replace('آینده', 'بعد')
    sentence = sentence.replace('قبل', 'پیش')
    # replace numbers
    sentence = sentence.replace("یک ", "1 ")
    sentence = sentence.replace("دو ", "2 ")
    sentence = sentence.replace("سه ", "3 ")
    sentence = sentence.replace("چهار ", "4 ")
    sentence = sentence.replace("پنج ", "5 ")
    sentence = sentence.replace("شش ", "6 ")
    sentence = sentence.replace("هفت ", "7 ")
    sentence = sentence.replace("هشت ", "8 ")
    sentence = sentence.replace("نه ", "9 ")
    sentence = sentence.replace("ده ", "10 ")
    sentence = sentence.replace("یازده ", "11 ")
    sentence = sentence.replace("دوازده ", "12 ")
    sentence = sentence.replace("سیزده ", "13 ")
    sentence = sentence.replace("چهارده ", "14 ")
    sentence = sentence.replace("پانزده ", "15 ")
    sentence = sentence.replace("شانزده ", "16 ")
    sentence = sentence.replace("هفده ", "17 ")
    sentence = sentence.replace("هجده ", "18 ")
    sentence = sentence.replace("نوزده ", "19 ")
    sentence = sentence.replace("بیست ", "20 ")
    sentence = sentence.replace("بیست و 1", "21")
    sentence = sentence.replace("بیست و 2", "22")
    sentence = sentence.replace("بیست و 3", "23")
    sentence = sentence.replace("بیست و 4", "24")
    sentence = sentence.replace("بیست و 5", "25")
    sentence = sentence.replace("بیست و 6", "26")
    sentence = sentence.replace("بیست و 7", "27")
    sentence = sentence.replace("بیست و 8", "28")
    sentence = sentence.replace("بیست و 9", "29")
    sentence = sentence.replace("سی ", "30 ")
    sentence = sentence.replace("سی و 1", "31")

    sentence = sentence.replace("پس فردا", "2 روز بعد")
    sentence = sentence.replace("پریروز", "2 روز پیش")

    if not re.findall(r"([\u0660-\u0669]|[\d])+[\s]سال[\s]بعد", sentence):
        sentence = sentence.replace("سال بعد", "1 سال بعد")
    if not re.findall(r"([\u0660-\u0669]|[\d])+[\s]سال[\s]پیش", sentence):
        sentence = sentence.replace("سال پیش", "1 سال پیش")

    if not re.findall(r"([\u0660-\u0669]|[\d])+[\s]هفته[\s]بعد", sentence):
        sentence = sentence.replace("هفته بعد", "1 هفته بعد")
    if not re.findall(r"([\u0660-\u0669]|[\d])+[\s]هفته[\s]پیش", sentence):
        sentence = sentence.replace("هفته پیش", "1 هفته پیش")

    if not re.findall(r"([\u0660-\u0669]|[\d])+[\s]روز[\s]بعد", sentence):
        sentence = sentence.replace("روز بعد", "1 روز بعد")
    if not re.findall(r"([\u0660-\u0669]|[\d])+[\s]روز[\s]پیش", sentence):
        sentence = sentence.replace("روز پیش", "1 روز پیش")

    sentence = sentence.replace("پریسال", "2 سال پیش")

    if not re.findall(r"([\u0660-\u0669]|[\d])+[\s]سال[\s]بعد", sentence):
        sentence = sentence.replace("سال بعد", "1 سال بعد")
    return sentence
