from datetime import datetime

import requests

from APIs.religious_time import ReligiousTime
from APIs.time import Time
from APIs.weather import Weather
from APIs.date import Date


def test_rel_time():
	rel_time = "اذان صبح"
	date = "2020-05-01"
	city = "تهران"
	
	try:
		datetime.strptime(date, "%Y-%m-%d")
	except ValueError:
		print("Invalid date format! Should be %Y-%m-%d")
		return
	
	rt = ReligiousTime(rel_time, city, date)
	result = rt.get_rel_timing()
	print(result)


def test_time():
	city = "شیراز"
	t = Time(city)
	x = t.send_request()
	print(x)


def test_weather():
	dt = "2020-12-22 21:49"
	city = "شیراز"
	
	try:
		datetime.strptime(dt, "%Y-%m-%d %H:%M")
	except ValueError:
		try:
			datetime.strptime(dt, "%Y-%m-%d")
		except ValueError:
			print("Invalid date format! Should be %Y-%m-%d or <%Y-%m-%d %H:%M>")
			return
	
	current_dt = int(datetime.timestamp(datetime.now()))
	w = Weather(city, dt, current_dt)
	res = w.send_request()
	print(res)
	
	
def test_date():
	# if date is not specified
	# date = datetime.strftime(datetime.now(), "%Y-%m-%d")
	date = "2020-12-22"
	d = Date("gregorian", "hijri", date)
	res = d.convert_date()
	print(res)
	

def main():
	# All the time formats are in "YYYY-MM-DD HH:MM" or "YYYY-MM-DD"
	# and THEY SHOULD BE GREGORIAN.
	test_date()
	

if __name__ == '__main__':
	main()
