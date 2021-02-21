from datetime import datetime
import random

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


def weather_sentence(result: dict, n_days: str = "") -> str:
    city = city_random(result["city"][0])
    date = "در تاریخ " + date_from_str(result["date"][0])
    time = result["time"][0] if result["time"] else None
    time_repl = date if n_days == "" else n_days
    if time is None:
        if 'ی' not in result["result"]:
            return random.choice([
                f"دمای هوای شهر {city}، {time_repl}، {result['result']} درجه است",
                f"{time_repl} میزان دمای شهر {city} برابر با {result['result']} درجه‌ی سانتی‌گراد است",
                f"درجه‌ی حرارت شهر {city}، {time_repl} برابر با {result['result']} درجه‌ی سانتی‌گراد است",
            ])
        else:
            return random.choice([
                f"وضعیت آب و هوایی شهر {city}، {time_repl} به صورت {result['result']} است",
                f"ساکنین شهر {city}، {time_repl} هوایی {result['result']} را تجربه می‌کنند",
                f"{time_repl} شهر {city} هوایی {result['result']} دارد",
            ])
    else:
        if 'ی' not in result["result"]:
            return random.choice([
                f"دمای هوای شهر {city}، {time_repl} در ساعت {time} برابر با {result['result']} درجه است",
                f"{time_repl} در ساعت {time} میزان دمای شهر {city} برابر با {result['result']} درجه‌ی سانتی‌گراد است",
                f"درجه‌ی حرارت شهر {city}، {time_repl} در ساعت {time} برابر با {result['result']} درجه‌ی سانتی‌گراد است",
            ])
        else:
            return random.choice([
                f"وضعیت آب و هوایی شهر {city}، {time_repl} در ساعت {time} به صورت {result['result']} است",
                f"ساکنین شهر {city}، {time_repl} در ساعت {time} هوایی {result['result']} را تجربه می‌کنند",
                f"{time_repl} در ساعت {time} شهر {city} هوایی {result['result']} دارد",
            ])


def weather_logical_sentence(result: dict, logic: str, n_days: str = "") -> str:
    city = city_random(result["city"][0])
    date = "در تاریخ " + date_from_str(result["date"][0])
    time = result["time"][0] if result["time"] else None
    time_repl = date if n_days == "" else n_days
    logic += "دمای هوای شهر"
    if time is None:
        return random.choice([
            f"{logic} {city}، {time_repl}، {result['result']} درجه است",
            f"{time_repl} {logic} {city} برابر با {result['result']} درجه‌ی سانتی‌گراد است",
            f"{logic} {city}، {time_repl} برابر با {result['result']} درجه‌ی سانتی‌گراد است",
        ])
    else:
        return random.choice([
            f"{logic} {city}، {time_repl} در ساعت {time} برابر با {result['result']} درجه است",
            f"{time_repl} در ساعت {time} {logic} {city} برابر با {result['result']} درجه‌ی سانتی‌گراد است",
            f"{logic} {city}، {time_repl} در ساعت {time} برابر با {result['result']} درجه‌ی سانتی‌گراد است",
        ])


def religion_sentence(result: dict) -> str:
    rel_time = result["religious_time"][0]
    city = result["city"][0]
    date = date_from_str(result["date"][0])
    return random.choice([
        f"{rel_time} به افق شهر {city} در تاریخِ {date}، ساعت {result['result']} است",
    ])


def time_sentence(result: dict, eq_string: str = None) -> str:
    city = city_random(result["city"][0])
    city_eq = city if eq_string is None else random.choice([eq_string, city])
    return random.choice([
        f"در {city_eq} الان ساعت {result['result']} است",
        f"ساعت فعلی {city_eq} در حال حاضر {result['result']} است",
        f"ساعت فعلی {city_eq} ، {result['result']} است",
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
            f"در سالِ {convert_year(result['result'].split('-')[0])} مناسبت {event} در روزِ {convert_day(result['result'].split('-')[2])} ماهِ {convert_month(int(result['result'].split('-')[1]))} است",
        ])
    else:
        if len(result["result"].split('-')) != 3:
            return random.choice([
                f"مناسبتِ روزِ {date_str}، {result['result']} است",
            ])
        else:

            if cal_type == "شمسی":
                # TODO calendars types
                return random.choice([
                    f"تاریخِ {choose_date(result['result'])} معادلِ تاریخِ {date_from_str(result['result'])} در تقویم {cal_type} است",
                    f"تاریخِ مدنظرِ شما معادلِ {date_from_str(result['result'])} است",
                ])
            elif cal_type == "قمری" or cal_type == "هجری":
                return random.choice([
                    f"تاریخِ شمسیِ {date_str} معادلِ تاریخِ {date_from_str_hijri(result['result'])} در تقویم {cal_type} است",
                ])
            elif cal_type == "میلادی":
                return random.choice([
                    f"تاریخِ شمسیِ {date_str} معادلِ تاریخِ {result['result']} در تقویم {cal_type} است",
                ])


def date_from_str(date_str):
    dates = date_str.split('-')
    year = convert_year(dates[0])
    month = convert_month(int(dates[1]))
    day = convert_day(dates[2])
    return day + "ِ  " + month + "ِ " + " سالِ " + year


def city_random(city):
    return_list = [
        f"{city}",
        f"شهر {city}"]
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
    return year


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
    return day + "ِ  " + month + "ِ " + " سالِ " + year


def choose_date(date_str):
    relative_date = relative_day(date_str)
    if relative_date == "":
        return date_from_str(date_str)
    else:
        return random.choice([date_from_str(date_str), relative_date, relative_date])


def relative_day(date_str):
    en_datetime = dateparser.parse('امروز',
                                   settings={'TIMEZONE': '+0330'})
    naive_dt = JalaliDate(en_datetime)
    d1 = datetime.strptime(date_str, "%Y-%m-%d")
    print(naive_dt)
    print(d1)
    difference_days = naive_dt.day - d1.day
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
