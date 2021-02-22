import random
from datetime import datetime

import dateparser
import num2fawords
from persiantools.jdatetime import JalaliDate

from capitals import capital_to_country


def convert_month(month: int) -> str:
    return ["فروردین", "اردی‌بهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر",
            "آبان", "آذر", "دی", "بهمن", "اسفند"][month - 1]


def convert_month_hijri(month: int) -> str:
    return ["محرم", "صفر", "ربیع‌الاَوَل", "ربیع‌الثانی", "جمادی‌الاول", "جمادی‌الثانی", "رجب",
            "شعبان", "رمضان", "شوال", "ذیعقده", "ذیحجه"][month - 1]


def convert_month_georgian(month: int) -> str:
    return ["ژانویه", "فوریه", "مارس", "آپریل", "می", "ژوئن", "جولای", "آگوست",
            "سپتامبر", "اکتبر", "نوامبر", "دسامبر"][month - 1]


def unknown_sentence() -> str:
    return random.choice([
        "سوال مطرح شده خارج از حیطه ی سوالات مسابقه است",
        "با توجه به حوزه‌ی سوالات مسابقه قادر به پاسخ‌گویی نیستیم",
        "سوال مورد نظر در هیچ دسته‌بندی‌ای جا نمی‌گیرد",
    ])


def weather_sentence(result: dict, logic='') -> str:
    city = city_random(result["city"][0])
    date = choose_date(result['date'][0])
    time1 = result["time"][0] if result["time"] else None
    time = result["religious_time"][0] if result["religious_time"] else time1
    if time is None:
        if 'ی' not in result["result"]:
            list_ret = [f"{logic} دمای هوایِ {city}، {date}، {result['result']} درجه {generate_verb()}"]
            if logic == '':
                list_ret.extend(
                    [f"{date}، میزانِ دمای {city} برابر با {result['result']} درجه‌ ی سانتی‌گراد {generate_verb()}",
                     f"درجه ی حرارتِ {city}، {date} برابر با {result['result']} درجه ‌یِ سانتی‌گراد {generate_verb()}"])
            return random.choice(list_ret)
        else:
            return random.choice([
                f"وضعیتِ آب و هوایی {city}، {date}، به صورتِ {result['result']} {generate_verb()}",
                f"ساکنینِ {city}، {date}، هوایی ، {result['result']} را تجربه می‌کنند",
                f"{date} ، {city}، هوایی {result['result']} دارد",
            ])
    else:
        if 'ی' not in result["result"]:
            list_ret = [
                f"{logic} دمایِ هوایِِ {city}، {date} در ساعتِ {time} برابر با {result['result']} درجه {generate_verb()}"]
            if logic == '':
                list_ret.extend([
                    f"{date} در ساعتِ {time} ، میزانِ دمای  {city} برابر با {result['result']} درجه‌ ی سانتی‌گراد {generate_verb()}",
                    f"درجه ‌ی حرارتِِ {city}، {date} در ساعتِ {time} ، برابر با {result['result']} درجه ‌ی سانتی‌گراد {generate_verb()}", ])
            return random.choice(list_ret)
        else:
            return random.choice([
                f"وضعیتِ آب و هوایی {city}، {date} در ساعتِ {time} به صورتِ {result['result']} {generate_verb()}",
                f"ساکنینِ {city}، {date} در ساعتِ {time} هوایی {result['result']} را تجربه می‌کنند",
                f"{date} در ساعتِ ، {time} ، {city} هوایی {result['result']} دارد",
            ])


def weather_logical_sentence(answer: dict, logic1='', logic2='', logic_mode='', answer_number=0) -> str:
    cities = ['', '']
    dates = ['', '']
    times = ['', '']
    times[0] = answer["time"][0] if answer["time"] else ''
    logics = [logic1, logic2]
    cities[0] = city_random(answer["city"][0])
    dates[0] = choose_date(answer['date'][0])

    other_answer_num = 1 if answer_number == 0 else 0
    if len(answer["city"]) == 2:
        cities[1] = city_random(answer["city"][1])
    else:
        cities[1] = city_random(answer["city"][0])
    if len(answer["date"]) == 2:
        dates[1] = choose_date(answer['date'][1])
    else:
        dates[1] = ''
    if len(answer["time"]) == 2:
        times[1] = answer["time"][1]
    else:
        times[1] = ''
    if logic_mode == 'اختلاف':
        if dates[1] == '':
            return_sen = f"اختلافِ {logics[0]} دمای هوای {cities[0]}،{times[0]} و {logics[1]} دمای {cities[1]}، {dates[1]}،{times[1]}  برابر با {answer['result']} {generate_verb()} "
        else:
            return_sen = f"اختلافِ {logics[0]} دمای هوای {cities[0]}، {dates[0]}،{times[0]} و {logics[1]} دمای {cities[1]}، {dates[1]}،{times[1]}  برابر با {answer['result']} {generate_verb()} "
    if logic_mode == 'سردتر' or logic_mode == 'گرمتر':
        if dates[answer_number] == '':
            return_sen = f"ِ{logics[answer_number]} دمای هوای {cities[answer_number]}،{times[answer_number]}  {logic_mode} از {logics[other_answer_num]} دمای {cities[other_answer_num]}، {dates[other_answer_num]}،{times[other_answer_num]} {generate_verb()}"
        else:
            return_sen = f"ِ{logics[answer_number]} دمای هوای {cities[answer_number]}، {dates[answer_number]} ،{times[answer_number]}  {logic_mode} از {logics[other_answer_num]} دمای {cities[other_answer_num]}، {dates[other_answer_num]}،{times[other_answer_num]} {generate_verb()} "
    return return_sen


def weather_difference_sentence() -> str:
    return ""


def religion_sentence(result: dict) -> str:
    rel_time = result["religious_time"][0]
    city = result["city"][0]
    date = date_from_str(result["date"][0])
    return random.choice([
        f"{rel_time} به افق شهر {city} در تاریخِ {date}، ساعت {result['result']} {generate_verb()}",
    ])


def time_sentence(result: dict, eq_string: str = None) -> str:
    city = city_random(result["city"][0])
    city_eq = city if eq_string is None else random.choice([eq_string, city])
    return random.choice([
        f"در {city_eq} الان ساعت {result['result']} {generate_verb()}",
        f"ساعت فعلی {city_eq} در حال حاضر {result['result']} {generate_verb()}",
        f"ساعت فعلی {city_eq} ، {result['result']} {generate_verb()}",
    ])


def date_sentence(result: dict) -> str:
    event = result["event"][0] if result["event"] else None
    if result["date"]:
        date_str = date_from_str(result["date"][0])
    else:
        date_str = None
    if result["calendar_type"]:
        cal_type = result["calendar_type"][0]
    else:
        cal_type = None

    if event is not None:
        return random.choice([
            f"در سالِ {convert_year(result['result'].split('-')[0])} مناسبت {event} در روزِ {convert_day(result['result'].split('-')[2])} ماهِ {convert_month(int(result['result'].split('-')[1]))} {generate_verb()}",
        ])
    else:
        if len(result["result"].split('-')) != 3:
            return random.choice([
                f"مناسبتِ روزِ {date_str}، {result['result']} {generate_verb()}",
            ])
        else:

            if cal_type == "شمسی":
                return random.choice([
                    f" {choose_date(result['result'], False)} معادلِ تاریخِ {date_from_str(result['result'])} در تقویم {cal_type} {generate_verb()}",
                    f"تاریخِ مدنظرِ شما معادلِ {date_from_str(result['result'])} {generate_verb()}",
                ])
            elif cal_type == "قمری" or cal_type == "هجری":
                return random.choice([
                    f"{choose_date(result['result'])} معادلِ تاریخِ {date_from_str_hijri(result['result'])} در تقویم {cal_type} {generate_verb()}",
                ])
            elif cal_type == "میلادی":
                return random.choice([
                    f"{date_str} معادلِ تاریخِ {date_from_str_georgian(result['result'])} در تقویم {cal_type} {generate_verb()}",
                ])


def date_from_str(date_str):
    dates = date_str.split('-')
    year = convert_year(dates[0])
    month = convert_month(int(dates[1]))
    day = convert_day(dates[2])
    return day + "ِ  " + month + "ِ " + year


def city_random(city):
    return_list = [
        f"{city}",
        f"{city}",
        f"{city}",
        f"شهر {city}",
        f"شهر {city}",
        f"شهر {city}", ]
    country_name = capital_to_country(city)
    if not country_name == "":
        country_name = country_name.split(" ")
        return_list.append("پایتخت " + country_name[1])
        return_list.append("مرکز " + country_name[1])
        return_list.append("مرکز کشور " + country_name[1])
        return_list.append("پایتخت کشور " + country_name[1])
    return random.choice(return_list)


def convert_day(day):
    day = int(day)
    days = num2fawords.ordinal_words(day).split(" و ")
    if len(days) == 2:
        day = days[0] + "و" + " " + days[1]
    else:
        day = days[0]
    if day == "سیم" :
        day = "سی‌اُم"
    return day


def convert_year(year):
    year_int = int(year)
    if year_int > 1399:
        years = num2fawords.words(year_int).split(" و ")
        year = ""
        for i in range(len(years) - 1):
            year = year + years[i] + "ُ" + " "
        year = year + years[-1] + " "
    else:
        year = year[2:]
    return_list = [year, " سالِ " + year]
    if year == "99":
        return_list.extend(["امسال"])
    if year == "98":
        return_list.extend([f"سال {previous_word()} "])
    if year == "1400":
        return_list.extend([f"سال {next_word()} "])
    return random.choice(return_list)


def date_from_str_hijri(date_str):
    dates = date_str.split('-')
    year = convert_year(dates[0])
    month = convert_month_hijri(int(dates[1]))
    day = convert_day(dates[2])
    return day + "ِ  " + month + "ِ " + " سالِ " + year


def date_from_str_georgian(date_str):
    dates = date_str.split('-')
    year = convert_year(dates[0])
    month = convert_month_georgian(int(dates[1]))
    day = convert_day(dates[2])
    return random.choice(
        [day + "ِ  " + month + "ِ " + " سالِ " + year,
         day + "ِ  " + " ماه " + month + "ِ " + " سالِ " + year])


def choose_date(date_str, is_date=True):
    relative_date = relative_day(date_str)
    if is_date:
        if relative_date == "":
            return random.choice(
                [date_from_str(date_str), f"در تاریخِ {date_from_str(date_str)}"])
        else:
            return random.choice(
                [date_from_str(date_str), f"در تاریخِ {date_from_str(date_str)}", relative_date, relative_date])
    else:
        if relative_date == "":
            return random.choice(
                [date_from_str(date_str), f"تاریخِ {date_from_str(date_str)}"])
        else:
            return random.choice(
                [date_from_str(date_str), f"تاریخِ {date_from_str(date_str)}", relative_date, relative_date])


def relative_day(date_str):
    en_datetime = dateparser.parse('امروز',
                                   settings={'TIMEZONE': '+0330'})
    naive_dt = JalaliDate(en_datetime)
    d1 = datetime.strptime(date_str, "%Y-%m-%d")
    difference_days = d1.day - naive_dt.day
    return {
        -30: random.choice([f'ماه {previous_word()}']),
        -14: random.choice([f'دو هقته‌ي {previous_word()}']),
        -7: random.choice([f'هقته‌ي {previous_word()}', f'یک هقته‌ي {previous_word()}']),
        -2: random.choice(['پریروز', f'دو روزِ {previous_word()}']),
        -1: random.choice(['دیروز', f'روزِ {previous_word()}']),
        0: random.choice(['امروز']),
        1: random.choice(['فردا', f'روزِ {next_word()}']),
        2: random.choice(['پس‌فردا', f'دو روزِ {next_word()}']),
        7: random.choice([f'هقته‌‌ي {next_word()}', f'یک هقته‌ی {next_word()}']),
        14: random.choice([f'دو هقته‌ي {next_word()}']),
        30: random.choice([f'ماهِ {next_word()}']),
    }.get(difference_days, '')


def next_word():
    return random.choice(['آینده', 'بعد'])


def previous_word():
    return random.choice(['قبل', 'گذشته'])


def generate_verb():
    return random.choice(["است", "می‌باشد", "اعلام می‌گردد"])
