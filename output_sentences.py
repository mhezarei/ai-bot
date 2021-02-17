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
                f"دمای هوای شهر {city} در تاریخ {date.split('-')}، {result['result']} درجه است.",
                f"در تاریخ {date.split('-')} میزان دمای شهر {city} برابر با {result['result']} درجه‌ی سانتی‌گراد است.",
                f"درجه‌ی حرارت شهر {city} در تاریخ {date.split('-')} برابر با {result['result']} درجه‌ی سانتی‌گراد است.",
            ])
        else:
            return random.choice([
                f"وضعیت آب و هوایی شهر {city} در تاریخ {date.split('-')} به صورت {result['result']} است.",
                f"ساکنین شهر {city} در تاریخ {date.split('-')} هوایی {result['result']} را تجربه می‌کنند.",
                f"در تاریخ {date.split('-')} شهر {city} هوایی {result['result']} دارد.",
            ])
    else:
        if 'ی' not in result["result"]:
            return random.choice([
                f"دمای هوای شهر {city} در تاریخ {date.split('-')} و ساعت {time} برابر با {result['result']} درجه است.",
                f"در تاریخ {date.split('-')} و ساعت {time} میزان دمای شهر {city} برابر با {result['result']} درجه‌ی سانتی‌گراد است.",
                f"درجه‌ی حرارت شهر {city} در تاریخ {date.split('-')} و ساعت {time} برابر با {result['result']} درجه‌ی سانتی‌گراد است.",
            ])
        else:
            return random.choice([
                f"وضعیت آب و هوایی شهر {city} در تاریخ {date.split('-')} و ساعت {time} به صورت {result['result']} است.",
                f"ساکنین شهر {city} در تاریخ {date.split('-')} و ساعت {time} هوایی {result['result']} را تجربه می‌کنند.",
                f"در تاریخ {date.split('-')} و ساعت {time} شهر {city} هوایی {result['result']} دارد.",
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
        f"dar shahre {city}, alan saat {result['result']} ast.",
        f"dar hale hazer dar {city}, saat {result['result']} ast.",
        f"saate felie shahre {city}, {result['result']} ast",
    ])


# def date_sentence(result: dict) -> str:
#     event = result["event"][0] if result["event"] else None
#
