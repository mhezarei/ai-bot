import random


def convert_month(month: int) -> str:
    return ["فروردین", "اردی‌بهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر",
            "آبان", "آذر", "دی", "بهمن", "اسفند"][month - 1]


def weather_sentence(result: dict) -> str:
    city = result["city"][0]
    date = result["date"][0]
    time = result["time"][0] if result["time"] else None
    if time is None:
        if 'ی' not in result["result"]:
            return random.choice([
                f"دمای هوای شهر {city} در تاریخ {date}، {result['result']} درجه است.",
                f"در تاریخ {date} میزان دمای شهر {city} برابر با {result['result']} درجه‌ی سانتی‌گراد است.",
                f"درجه‌ی حرارت شهر {city} در تاریخ {date} برابر با {result['result']} درجه‌ی سانتی‌گراد است.",
            ])
        else:
            return random.choice([
                f"وضعیت آب و هوایی شهر {city} در تاریخ {date} به صورت {result['result']} است.",
                f"ساکنین شهر {city} در تاریخ {date} هوایی {result['result']} را تجربه می‌کنند.",
                f"در تاریخ {date} شهر {city} هوایی {result['result']} دارد.",
            ])
    else:
        if 'ی' not in result["result"]:
            return random.choice([
                f"دمای هوای شهر {city} در تاریخ {date} و ساعت {time} برابر با {result['result']} درجه است.",
                f"در تاریخ {date} و ساعت {time} میزان دمای شهر {city} برابر با {result['result']} درجه‌ی سانتی‌گراد است.",
                f"درجه‌ی حرارت شهر {city} در تاریخ {date} و ساعت {time} برابر با {result['result']} درجه‌ی سانتی‌گراد است.",
            ])
        else:
            return random.choice([
                f"وضعیت آب و هوایی شهر {city} در تاریخ {date} و ساعت {time} به صورت {result['result']} است.",
                f"ساکنین شهر {city} در تاریخ {date} و ساعت {time} هوایی {result['result']} را تجربه می‌کنند.",
                f"در تاریخ {date} و ساعت {time} شهر {city} هوایی {result['result']} دارد.",
            ])


def religion_sentence(result: dict) -> str:
    rel_time = result["religious_time"][0]
    city = result["city"][0]
    date = result["date"][0]
    return random.choice([
        f"اوقات شرعی {rel_time} به افق شهر {city} در تاریخ {date}، ساعت {result['result']} است.",
    ])


def time_sentence(result: dict) -> str:
    city = result["city"][0]
    return random.choice([
        f"در شهر {city} الان ساعت {result['result']} است.",
        f"ساعت فعلی شهر {city} در حال حاضر {result['result']} است.",
        f"ساعت فعلی شهر {city} فلان، {result['result']} است.",
    ])


def date_sentence(result: dict) -> str:
    event = result["event"][0] if result["event"] else None
    date = result["date"][0] if result["date"] else None
    cal_type = result["calender_type"][0] if result["calender_type"] else None
    if event is not None:
        return random.choice([
            f"در سال {result['result'].split('-')[0]} مناسبت {event} در روز {result['result'].split('-')[2]} و ماه {result['result'].split('-')[1]} است.",
        ])
    else:
        if len(result["result"].split('-')) != 3:
            return random.choice([
                f"مناسبت روز {date.split('-')[2]} از ماه {date.split('-')[1]} از سال {date.split('-')[0]}، {result['result']} است.",
            ])
        else:
            return random.choice([
                f"تاریخ شمسی {date} معادل تاریخ {result['result']} در تقویم {cal_type} است.",
            ])
