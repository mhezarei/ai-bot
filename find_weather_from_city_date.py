from weather import Weather
from datetime import datetime


def find_weather_from_city_date(Question, city, greg_date):
    current_dt = int(datetime.timestamp(datetime.now()))
    cond = ""
    max_list = ["حداکثر", "بیشترین", "گرمترین", "گرم‌ترین", "گرم ترین"]
    min_list = ["حداقل", "کمترین", "کمینه"]
    mid_list = ["میانگین"]
    for elem in min_list:
        if elem in Question:
            w = Weather(city, greg_date, current_dt, True)
            out = w.send_request()
            temp = out[0]
            return float(temp), cond, w.url
    for elem in max_list:
        if elem in Question:
            w = Weather(city, greg_date, current_dt, True)
            out = w.send_request()
            temp = out[1]
            return float(temp), cond, w.url
    for elem in mid_list:
        if elem in Question:
            w = Weather(city, greg_date, current_dt, True)
            out = w.send_request()
            temp = out[2]
            return float(temp), cond, w.url
    w = Weather(city, greg_date, current_dt)
    temp, cond = w.send_request()
    return float(temp), cond, w.url
