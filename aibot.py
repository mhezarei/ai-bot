from datetime import datetime
from find import find
from learning import predict
from weather import Weather
from religious_time import ReligiousTime
from mhr_time import Time
from date import Date
from utility import convert_date


class BOT:
    def __init__(self):
        self.modified = False

    def is_modified(self):
        return self.modified

    '''
    This method takes an string as input, the string contains the string of question.
    If you are using this method, we presume that you want to use nevisa and ariana.
    
    :Param Question : an string containing the question.

    : return : A dictionary containing the type of question, corresponding arguments, api_url and result.
    '''

    def AIBOT(self, Question):
        answer = {'type': '0', 'city': [], 'date': [],
                  'time': [], 'religious_time': [], 'calendar_type': [],
                  'event': [], 'api_url': [], 'result': ''}
        '''
        You should implement your code right here.
        '''

        answer, method = find(Question)
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
                current_dt = int(datetime.timestamp(datetime.now()))
                w = Weather(answer["city"][0], greg_date, current_dt)
                temp, cond = w.send_request()
                if method == "temp":
                    answer["result"] = temp
                elif method == "cond":
                    answer["result"] = cond
                answer["api_url"] = [w.url]
            except Exception:
                # raise ValueError("Type 1 Error!")
                pass

        elif answer["type"] == '2':
            try:
                greg_date = convert_date(answer["date"][0], "shamsi",
                                         "greg")
                rl = ReligiousTime(answer["religious_time"][0], answer["city"][0],
                                   greg_date)
                res = rl.get_rel_timing()
                answer["result"] = res
                answer["api_url"] = [rl.url]
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
            try:
                answer["api_url"] = ["https://www.time.ir/"]

                if answer["calendar_type"] and answer["date"]:
                    target = answer["calendar_type"][0]
                    if target == "شمسی":
                        answer["result"] = convert_date(answer["date"][0],
                                                        "shamsi", "shamsi")
                    elif target == "قمری":
                        answer["result"] = convert_date(answer["date"][0],
                                                        "shamsi", "hijri")
                    elif target == "میلادی":
                        answer["result"] = convert_date(answer["date"][0],
                                                        "shamsi", "greg")

                if answer["date"]:
                    answer["result"] = answer["date"][0]
            except Exception:
                # raise ValueError("Type 4 Error!")
                pass
        elif answer["type"] == '-1':
            answer = {'type': '-1', 'city': [], 'date': [],
                      'time': [], 'religious_time': [], 'calendar_type': [],
                      'event': [], 'api_url': [], 'result': ''}

        return answer

    '''
    This method takes an string as input, the string contains the address of a wav file.
    You can either use your own speech recognition or nevisa to extract the question from that file.
    Also you should call ariana to create an audio file as output.
    
    :Param Address : an string containing the the address of a wav file.

    : return : A dictionary containing the type of question, corresponding arguments, api_url and result.
    '''

    def AIBOT_Modified(self, Address):
        answer = {'type': '0', 'city': [], 'date': [],
                  'time': [], 'religous_time': [], 'calendar_type': [],
                  'event': [], 'api_url': '', 'result': ''}
        '''
        You should implement your code right here.
        '''
        return answer
