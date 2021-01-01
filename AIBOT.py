from datetime import datetime
from find_args.find import find
from Intents.learning import predict
from APIs.weather import Weather
from APIs.religious_time import ReligiousTime
from APIs.time import Time
from APIs.date import Date
from APIs.utility import convert_date


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
		answer["type"] = str(predict(Question))
		
		if answer["type"] == '1':
			# HANDLED BY ARGUMENTS
			# method = "temp"
			
			current_dt = int(datetime.timestamp(datetime.now()))
			w = Weather(answer["city"][0], answer["date"][0], current_dt)
			temp, cond = w.send_request()
			
			if method == "temp":
				answer["result"] = temp
			elif method == "cond":
				answer["result"] = cond
			
			answer["api_url"] = [w.url]
		elif answer["type"] == '2':
			rl = ReligiousTime(answer["religious_time"][0], answer["city"][0],
			                   answer["date"][0])
			res = rl.get_rel_timing()
			answer["result"] = res
			answer["api_url"] = [rl.url]
		elif answer["type"] == '3':
			t = Time(answer["city"][0])
			res = t.send_request()
			answer["result"] = res
			answer["api_url"] = [t.url]
		elif answer["type"] == '4':
			answer["api_url"] = ["https://www.time.ir/"]
			
			if answer["calender_type"] and answer["date"]:
				target = answer["calender_type"][0]
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
