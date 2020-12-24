import json

import requests

from APIs.utility import *


class Weather:
	def __init__(self, city: str, dt: str, current_dt: int):
		self.city, self.country = get_english_names(city)
		self.lat, self.lon = get_lat_lon(self.city)
		# self.year, self.month, self.day, self.hour, self.minute = split_datetime(dt)
		self.dt = parse_datetime(dt)
		self.current_dt = current_dt
		self.current_url = "api.openweathermap.org/data/2.5/weather?appid=345d8217035c76f9bd352963c9f009a7&"
		self.forecast_url = "https://api.openweathermap.org/data/2.5/onecall?appid=345d8217035c76f9bd352963c9f009a7&"
		self.history_url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?appid=345d8217035c76f9bd352963c9f009a7&"
	
	# current weather IDK this yet
	
	# minute forecast for 1 hour
	# hourly forecast for 2 days
	# daily forecast for 7 days
	# historical for 5 days
	
	def send_request(self):
		if abs(self.dt - self.current_dt) >= 5 * 3600:
			return "The requested time must be within the last 5 days!"
		elif self.dt < self.current_dt:
			url = self.history_url + '&'.join(
				["lat=" + str(self.lat), "lon=" + str(self.lon),
				 "dt=" + str(self.dt), "units=metric"])
			print(url)
			return self.parse_history(requests.get(url).json())
	
	def parse_history(self, data) -> Tuple[str, int]:
		print(json.dumps(data, indent=1))
		print("Temp =", data["current"]["temp"])
		cond = data["current"]["weather"].lower()
		cond_num = -1
		if "cloud" in cond:
			cond_num = 1
		elif "rain" in cond:
			cond_num = 2
		elif "clear" in cond:
			cond_num = 3
		elif "snow" in cond:
			cond_num = 4
		elif "storm" in cond:
			cond_num = 5
		return cond, cond_num
