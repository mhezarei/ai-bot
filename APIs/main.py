from datetime import datetime
from APIs.religious_time import ReligiousTime
from APIs.time import Time
from APIs.weather import Weather


def test_rel_time():
	# assuming that the time format is "YYYY-MM-DD" and IT SHOULD BE GREGORIAN.
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
	# assuming that the time format is "YYYY-MM-DD HH:MM" or "YYYY-MM-DD"
	# and IT SHOULD BE GREGORIAN.
	dt = "2020-12-20"
	city = "مسکو"
	
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
	w.send_request()


def main():
	test_weather()
	# print(datetime.timestamp(datetime.now()))
	

if __name__ == '__main__':
	main()
