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
                f"damaye havaye {city} dar tarikhe {date.split('-')} {result['result']} daraje ast.",
                f"darajeye hararate {city} dar tarikhe {date.split('-')} {result['result']} darajeye santigrad ast.",
                f"dar tarikhe {date.split('-')}, shahre {city} damaye {result['result']} daraje darad.",
            ])
        else:
            return random.choice([
                f"{city} dar tarikhe {date.split('-')} {result['result']} ast.",
                f"vaziiate havaye {city} {date.split('-')} {result['result']} ast.",
                f"dar tarikhe {date.split('-')}, shahre {city} havaii {result['result']} darad.",
            ])
    else:
        if 'ی' not in result["result"]:
            return random.choice([
                f"damaye havaye {city} dar tarikhe {date.split('-')} va saate {time} {result['result']} daraje ast.",
                f"darajeye hararate {city} dar tarikhe {date.split('-')} va saate {time} {result['result']} darajeye santigrad ast.",
                f"dar tarikhe {date.split('-')} va saate {time}, shahre {city} damaye {result['result']} daraje darad.",
            ])
        else:
            return random.choice([
                f"{city} dar tarikhe {date.split('-')} va saate {time} {result['result']} ast.",
                f"vaziiate havaye {city} {date.split('-')} va saate {time} {result['result']} ast.",
                f"dar tarikhe {date.split('-')} va saate {time}, shahre {city} havaii {result['result']} darad.",
            ])


def religion_sentence(result: dict) -> str:
    rel_time = result["religious_time"][0]
    city = result["city"][0]
    date = result["date"][0]
    return random.choice([
        f"{rel_time} be ofoghe shahre {city} dar tarikhe {date}, {result['result']} ast.",
        f"{rel_time} shahre {city} movarekhe {date} saate {result['result']} ast.",
        f"dar tarikhe {date}, {rel_time} be vaghte {city} {result['result']} ast.",
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
