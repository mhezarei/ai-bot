from datetime import datetime

from Intents.learning import predict
from APIs.weather import Weather


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
                  'time': [], 'religious_time': [], 'calendar_type': [], 'event': [], 'api_url': '', 'result': ''}
        '''
        You should implement your code right here.
        '''
        
        answer["type"] = predict(Question)
        
        if answer["type"] == 1:
            # HANDLED BY ARGUMENTS
            method = "temp"
            date = "2020-12-29"
            city = "تهران"
            
            answer["date"] = [date]
            answer["city"] = [city]

            current_dt = int(datetime.timestamp(datetime.now()))
            w = Weather(answer["city"][0], answer["date"][0], current_dt)
            temp, cond = w.send_request()
            
            if method == "temp":
                answer["result"] = temp
            elif method == "cond":
                answer["result"] = cond
                
            answer["api_url"] = [w.url]
        elif answer["type"] == 2:
            pass
        elif answer["type"] == 3:
            pass
        elif answer["type"] == 4:
            pass
        
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
                  'time': [], 'religous_time': [], 'calendar_type': [], 'event': [], 'api_url': '', 'result': ''}
        '''
        You should implement your code right here.
        '''
        return answer
