from find_weather_from_city_date import find_weather_from_city_date
from utility import convert_date
from datetime import datetime


def weather_difference(Question, answer, str_separator):
    sentences = Question.split(str_separator)
    temps = []
    urls = []
    greg_date0 = convert_date(answer["date"][0], "shamsi",
                              "greg") + " " + answer["time"][0]
    temp, cond, url1 = find_weather_from_city_date(sentences[0], answer["city"][0], greg_date0)
    temps.append(temp)
    urls.append(url1)
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
    greg_date1 = convert_date(date1, "shamsi",
                              "greg") + " " + time1
    # TODO IF CITY ARE SAME
    temp, cond, url2 = find_weather_from_city_date(sentences[1], city, greg_date1)
    temps.append(temp)
    urls.append(url2)
    return temps, urls
