import re
import dateparser
from persiantools.jdatetime import JalaliDate
from dateparser.calendars.jalali import JalaliCalendar
from unidecode import unidecode
from persian_num_change import persian_num_change


def find_date_time(tokens_lem, sentence):
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
            numbers = [x.group() for x in re.finditer(r'([\u0660-\u0669]|[\d])+', string)]
            raw_hour = numbers[0]
            raw_minutes = numbers[1] if len(numbers) == 2 else '0'

            if "بعد از ظهر" in string or "عصر" in string or "شب" in string:
                if int(raw_hour) < 12:
                    raw_hour = str(int(raw_hour) + 12)
            if "بامداد" in string or "صبح" in string:
                if int(raw_hour) > 12:
                    raw_hour = str(int(raw_hour) - 12)
            if "و نیم" in string:
                raw_minutes = '30'
            elif "و ربع" in string:
                raw_minutes = '15'
            times.append(raw_hour.zfill(2) + ':' + raw_minutes.zfill(2))

    times = [unidecode(time) for time in times]
    print("times : " + str(times))

    return times

def reformat_date_time(string):

  def get_num(num):
    persian_num = persian_num_change(num)
    persian_num.results()
    return persian_num.num

  string = string.replace('ربع ', '15 دقیقه')
  string = string.replace('نیم ', '30 دقیقه')

  """ ساعت 3 و بیست و دو دقیقه """
  numbers = [x.group() for x in re.finditer(r"ساعت ([\u0660-\u0669]|\d)+ و ((([\u0600-\u0659]|[\u0670-\u06EF])+ دقیقه)|(([\u0600-\u0659]|[\u0670-\u06EF])+ و ([\u0600-\u0659]|[\u0670-\u06EF])+ دقیقه))", string)]
  for number in numbers:
    to_replace = number.replace('ساعت ', '')
    number = number.replace('ساعت ', '')
    number = number.replace(' دقیقه', '')
    numbers = number.split(' و ', maxsplit=1)
    string = string.replace(to_replace, f'{str(unidecode(numbers[0])).zfill(2)}:{str(get_num(numbers[1])).zfill(2)}')

  """ ساعت نه و 22 دقیقه """
  numbers = [x.group() for x in re.finditer(r"ساعت ([\u0600-\u0659]|[\u0670-\u06EF])+ و (([\u0660-\u0669]|\d)+ دقیقه)", string)]
  for number in numbers:
    to_replace = number.replace('ساعت ', '')
    number = number.replace('ساعت ', '')
    number = number.replace(' دقیقه', '')
    numbers = number.split(' و ', maxsplit=1)
    string = string.replace(to_replace, f'{str(get_num(numbers[0])).zfill(2)}:{str(unidecode(numbers[1])).zfill(2)}')

  """ ساعت نه و بیست و دو دقیقه """
  numbers = [x.group() for x in re.finditer(r"ساعت ([\u0600-\u0659]|[\u0670-\u06EF])+ و ((([\u0600-\u0659]|[\u0670-\u06EF])+ دقیقه)|(([\u0600-\u0659]|[\u0670-\u06EF])+ و ([\u0600-\u0659]|[\u0670-\u06EF])+ دقیقه))", string)]
  for number in numbers:
    to_replace = number.replace('ساعت ', '')
    number = number.replace('ساعت ', '')
    number = number.replace(' دقیقه', '')
    numbers = number.split(' و ', maxsplit=1)
    string = string.replace(to_replace, f'{str(get_num(numbers[0])).zfill(2)}:{str(get_num(numbers[1])).zfill(2)}')

  """ ساعت نه"""
  numbers = [x.group() for x in re.finditer(r"ساعت ([\u0600-\u0659]|[\u0670-\u06EF])+", string)]
  for number in numbers:
    to_replace = number.replace('ساعت ', '')
    number = number.replace('ساعت ', '')
    try:
      string = string.replace(to_replace, f'{str(get_num(number))}:00')
    except KeyError:
      pass

  """ ساعت 9 و 22 دقیقه"""
  numbers = [x.group() for x in re.finditer(r"ساعت ([\u0660-\u0669]|\d)+ و (([\u0660-\u0669]|\d)+ دقیقه)", string)]
  for number in numbers:
    to_replace = number.replace('ساعت ', '')
    number = number.replace('ساعت ', '')
    number = number.replace(' دقیقه', '')
    numbers = number.split(' و ')
    string = string.replace(to_replace, f'{str(unidecode(numbers[0])).zfill(2)}:{str(unidecode(numbers[1])).zfill(2)}')
    print(string)

  """ ساعت 5 """
  numbers = [x.group() for x in re.finditer(r"ساعت ([\u0660-\u0669]|\d)+ ", string)]
  for number in numbers:
    to_replace = number.replace('ساعت ', '')
    number = number.replace('ساعت ', '')
    string = string.replace(to_replace, f'{str(unidecode(number)).zfill(2)}:00 ')

  return string