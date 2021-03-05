import time

from transformers import AutoTokenizer, AutoModelForTokenClassification

from answer_per_question import answer_per_question
from aryana import aryana
from auto_correct import auto_correct
from find_dates import reformat_date
from find_events_in_sentence import find_events_in_sentence
from find_time import reformat_date_time
from speechRec import google
from split import split


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
        answer = {'type': [], 'city': [], 'date': [],
                  'time': [], 'religious_time': [], 'calendar_type': [],
                  'event': [], 'api_url': [], 'result': []}
        answer_set = {'type': set(), 'city': set(), 'date': set(),
                      'time': set(), 'religious_time': set(), 'calendar_type': set(),
                      'event': set(), 'api_url': set(), 'result': []}
        # Question = auto_correct(Question)
        try:
            Question = reformat_date_time(Question)
        except:
            pass

        try:
            Question = reformat_date(Question)
        except:
            pass

        '/var/www/AIBot/media/codes/user_zivdar1matin@gmail.com/bert-base-parsbert-ner-uncased'
        tokenizer = AutoTokenizer.from_pretrained(
            '/var/www/AIBot/media/codes/user_zivdar1matin@gmail.com/bert-base-parsbert-ner-uncased')
        model = AutoModelForTokenClassification.from_pretrained(
            '/var/www/AIBot/media/codes/user_zivdar1matin@gmail.com/bert-base-parsbert-ner-uncased')

        try:
            events, event_keys = find_events_in_sentence(Question)
        except:
            events = []
            event_keys = []

        try:
            Questions = split(Question, events)
        except:
            Questions = [Question]
            pass

        final_answer = ""
        for sentence in Questions:
            q_answer, answer_sen = answer_per_question(sentence, model, tokenizer, events, event_keys)
            if final_answer == "":
                final_answer = answer_sen
            else:
                final_answer = final_answer + " و " + answer_sen
            for key in answer_set.keys():
                if key == "type":
                    answer_set[key].add(q_answer[key])
                elif key == "result":
                    if not q_answer[key] == "":
                        answer_set[key].append(q_answer[key])
                else:
                    answer_set[key].update(q_answer[key])
        for key in answer.keys():
            answer[key] = list(answer_set[key])
        final_answer = final_answer + " ."

        return answer, final_answer

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

        file = open(Address, mode='rb')

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

        answer, generated_sentence = self.AIBOT(text)

        response = aryana(generated_sentence)

        with open("response.wav", mode='bw') as f:
            f.write(response.content)

        return answer, response
