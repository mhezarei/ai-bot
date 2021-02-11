import time

from datetime import datetime
from find import find
from learning import predict
from weather import Weather
from religious_time import ReligiousTime
from mhr_time import Time
from date import Date
from utility import convert_date

from deepmine import Deepmine
from aryana import aryana
from nevisa import nevisa
from speechRec import google

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
    This method takes an string as input, the string contains the address of .wav file.
    
    :Param Address : an string containing the path of .wav file.

    : return : A dictionary containing the type of question, corresponding arguments, api_url and result.
    Also you should return your generated sentences as data stream. which mean what aryana returns.
    '''

    def aibot(self, Address):
        answer = {'type': [], 'city': [], 'date': [],
                  'time': [], 'religious_time': [], 'calendar_type': [], 'event': [], 'api_url': [''], 'result': []}
        '''
        You should implement your code right here.
        '''

        start = time.time()

        file=open(Address,mode='rb')

        """ Google """
        text = google(file)


        """ Nevisa """
        # comment="0024399744"
        # text = nevisa(file,comment)


        """ Deepmine """
        # #Create instance Deepmine()
        # m = Deepmine()
        # # get text of your file! return status,text: if status==0 error occured.
        # status,text = m.get_text(Address)

        print("Text::", text)

        end = time.time()
        print(f"Runtime of the speechRecognition API is {end - start}")
        
        answer = self.AIBOT(text)

        start = time.time()

        generated_sentence = "این یک جمله‌ای صرفا برای امتحان کردن است"
        response = aryana(generated_sentence)


        end = time.time()
        print(f"Runtime of the text-to-speech API is {end - start}")

        with open("response.wav", mode='bw') as f:
            f.write(response.content)

        return answer, response