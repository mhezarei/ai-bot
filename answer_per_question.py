from find import find
from find_fit_word import find_fit_word
from find_time_from_religious import find_time_from_religious
from find_weather_from_city_date import find_weather_from_city_date
from learning import predict
from mhr_time import Time
from output_sentences import religion_sentence, time_sentence, date_sentence, unknown_sentence, weather_sentence
from utility import convert_date
from weather_difference import weather_difference
import datetime


def answer_per_question(Question, model, tokenizer, all_events, all_event_keys):
    answer, method = find(Question, model, tokenizer, all_events, all_event_keys)
    answer_sentence = ""
    try:
        answer["type"] = str(predict(Question))
    except Exception:
        raise ValueError("Type Predict Error!")

    if answer["type"] == '1':
        # HANDLED BY ARGUMENTS
        # method = "temp"
        time_len = len(answer["time"])
        if answer["religious_time"]:
            time, answer["api_url"] = find_time_from_religious(answer)
            answer["time"].extend(time)
        if not answer["time"]:
            hour = datetime.datetime.now().hour
            if hour < 12:
                answer["time"] = ["12:00"]
            else:
                if (hour + 1) == 24:
                    hour = 0
                time = str(
                    str(hour + 1).zfill(2) + ":" + str(datetime.datetime.now().minute).zfill(2))
                answer["time"] = [time]
                print("time : " + str(answer["time"]))

        try:
            answer_mode = 0
            if "اختلاف" in Question or "تفاوت" in Question:
                temps, urls = weather_difference(Question, answer, ' و ')
                print(str(temps[0]) + "      ---    " + str(temps[1]))
                temp = round(abs(temps[1] - temps[0]), 2)
                answer_mode = 1
            elif "سردتر " in Question or "سرد تر " in Question:
                temps, urls = weather_difference(Question, answer, ' یا ')
                print(str(temps[0]) + "      ---    " + str(temps[1]))
                if temps[1] < temps[0]:
                    temp = find_fit_word(answer, True)
                else:
                    temp = find_fit_word(answer, False)
                answer_mode = 2
            elif "گرم‌تر " in Question or "گرمتر " in Question or "گرم تر " in Question:
                temps, urls = weather_difference(Question, answer, ' یا ')
                print(str(temps[0]) + "      ---    " + str(temps[1]))
                if temps[1] > temps[0]:
                    temp = find_fit_word(answer, True)
                else:
                    temp = find_fit_word(answer, False)
                answer_mode = 3
            else:
                greg_date = convert_date(answer["date"][0], "shamsi",
                                         "greg") + " " + answer["time"][0]
                temp, cond, url = find_weather_from_city_date(Question, answer["city"][0], greg_date)
                urls = [url]
                answer_mode = 4
            answer["api_url"].extend(urls)
            if method == "temp":
                answer["result"] = str(temp)
            elif method == "cond":
                answer["result"] = cond

            if answer["religious_time"]:
                answer["time"] = []
            if time_len == 0:
                answer["time"] = []
            else:
                answer["time"] = answer[:time_len]
            if answer_mode == 0:
                pass
            elif answer_mode == 1:
                pass
            elif answer_mode == 2:
                pass
            elif answer_mode == 3:
                pass
        except Exception:
            # raise ValueError("Type 1 Error!")
            pass

    elif answer["type"] == '2':
        try:
            result, answer["api_url"] = find_time_from_religious(answer)
            answer["result"] = result[0]
            answer_sentence = religion_sentence(answer)
        except Exception:
            # raise ValueError("Type 2 Error!")
            pass
    elif answer["type"] == '3':
        try:
            t = Time(answer["city"][0])
            res = t.send_request()
            answer["result"] = res
            answer["api_url"] = [t.url]
            answer["date"] = []
            answer["time"] = []
            answer_sentence = time_sentence(answer)
        except Exception:
            # raise ValueError("Type 3 Error!")
            pass
    elif answer["type"] == '4':
        answer["city"] = []
        try:
            answer["api_url"] = ["https://www.time.ir/"]
            if 'مناسبت' in Question:
                answer["result"] = answer["event"][0]
                answer["event"] = []
            else:
                if answer["calendar_type"] and answer["date"]:
                    target = answer["calendar_type"][0]
                    print(target)
                    if target == "شمسی":
                        answer["result"] = convert_date(answer["date"][0],
                                                        "shamsi", "shamsi")
                    elif target == "قمری" or target == "هجری":
                        answer["result"] = convert_date(answer["date"][0],
                                                        "shamsi", "hijri")
                    elif target == "میلادی":
                        answer["result"] = convert_date(answer["date"][0],
                                                        "shamsi", "greg")
                elif answer["date"]:
                    answer["result"] = answer["date"][0]
            answer_sentence = date_sentence(answer)
        except Exception:
            # raise ValueError("Type 4 Error!")
            pass
    elif answer["type"] == '-1':
        answer = {'type': '-1', 'city': [], 'date': [],
                  'time': [], 'religious_time': [], 'calendar_type': [],
                  'event': [], 'api_url': [], 'result': ''}
        answer_sentence = unknown_sentence()

    return answer, answer_sentence
