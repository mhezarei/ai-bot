from find_weather_from_city_date import find_weather_from_city_date
from utility import convert_date


def weather_difference(Question, answer, str_separator):
    sentences = Question.split(str_separator)
    temps = []
    urls = []
    greg_date0 = convert_date(answer["date"][0], "shamsi",
                              "greg") + " " + answer["time"][0]
    temp, cond, url1, logic1 = find_weather_from_city_date(sentences[0], answer["city"][0], greg_date0)
    temps.append(temp)
    urls.append(url1)
    city, date1, time1 = extract_second(answer)
    greg_date1 = convert_date(date1, "shamsi",
                              "greg") + " " + time1
    weather_words = ["حداکثر", "بیشترین", "گرمترین", "گرم‌ترین",
                     "گرم ترین", "حداقل", "کمترین", "کمینه", "میانگین",
                     'دما', 'درجه', 'اندازه', 'چقدر', 'میزان']
    sentence1 = ""
    for elem in weather_words:
        if elem in sentences[1]:
            sentence1 = sentences[1]
    if not sentence1:
        sentence1 = sentences[0]
    temp, cond, url2, logic2 = find_weather_from_city_date(sentence1, city, greg_date1)
    temps.append(temp)
    urls.append(url2)
    return temps, urls, logic1, logic2


def extract_second(answer):
    if len(answer["city"]) == 2:
        city = answer["city"][1]
    else:
        city = answer["city"][0]
    if len(answer["date"]) == 2:
        date1 = answer["date"][1]
    else:
        date1 = answer["date"][0]
    if len(answer["time"]) == 2:
        time1 = answer["time"][1]
    else:
        time1 = answer["time"][0]
    return city, date1, time1
