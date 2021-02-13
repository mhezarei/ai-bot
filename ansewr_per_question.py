from datetime import datetime
from find import find
from find_time_from_religious import find_time_from_religious
from learning import predict
from weather import Weather
from religious_time import ReligiousTime
from mhr_time import Time
from utility import convert_date


def answer_per_question(Question, model, tokenizer):
    answer, method = find(Question, model, tokenizer)
    try:
        answer["type"] = str(predict(Question))
    except Exception:
        raise ValueError("Type Predict Error!")

    if answer["type"] == '1':
        # HANDLED BY ARGUMENTS
        # method = "temp"
        greg_date = convert_date(answer["date"][0], "shamsi",
                                 "greg")
        print(answer["date"][0])
        try:
            if answer["religious_time"]:
                time, url = find_time_from_religious(answer)
                answer["time"].append(time)
                answer["api_url"].append(url)
            current_dt = int(datetime.timestamp(datetime.now()))
            w = Weather(answer["city"][0], greg_date, current_dt)
            temp, cond = w.send_request()
            if method == "temp":
                answer["result"] = temp
            elif method == "cond":
                answer["result"] = cond
            answer["api_url"].append(w.url)
            if answer["religious_time"]:
                answer["time"] = []
        except Exception:
            # raise ValueError("Type 1 Error!")
            pass

    elif answer["type"] == '2':
        try:
            answer["result"], answer["api_url"] = find_time_from_religious(answer)
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
        except Exception:
            # raise ValueError("Type 3 Error!")
            pass
    elif answer["type"] == '4':
        answer["city"] = []
        try:
            answer["api_url"] = ["https://www.time.ir/"]
            if 'مناسبت' in Question:
                answer["result"] = answer["event"]
                answer["event"] = []
            else:
                if answer["calendar_type"] and answer["date"]:
                    target = answer["calendar_type"][0]
                    print(target)
                    if target == "شمسی":
                        answer["result"] = convert_date(answer["date"][0],
                                                        "shamsi", "shamsi")
                    elif target == "قمری":
                        answer["result"] = convert_date(answer["date"][0],
                                                        "shamsi", "hijri")
                    elif target == "میلادی":
                        answer["result"] = convert_date(answer["date"][0],
                                                        "shamsi", "greg")
                elif answer["date"]:
                    answer["result"] = answer["date"][0]
        except Exception:
            # raise ValueError("Type 4 Error!")
            pass
    elif answer["type"] == '-1':
        answer = {'type': '-1', 'city': [], 'date': [],
                  'time': [], 'religious_time': [], 'calendar_type': [],
                  'event': [], 'api_url': [], 'result': ''}

    return answer
