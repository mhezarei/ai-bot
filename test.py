from datetime import datetime
from religious_time import ReligiousTime
from mhr_time import Time
from weather import Weather
from date import Date


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
	dt = "2020-12-26 21:49"
	city = "دوشنبه"
	
	try:
		datetime.strptime(dt, "%Y-%m-%d %H:%M")
	except ValueError:
		try:
			datetime.strptime(dt, "%Y-%m-%d")
		except ValueError:
			print(
				"Invalid date format! Should be %Y-%m-%d or <%Y-%m-%d %H:%M>")
			return
	
	current_dt = int(datetime.timestamp(datetime.now()))
	w = Weather(city, dt, current_dt)
	res = w.send_request()
	print(res[0])
	print(res[1])


def test_date():
	# if date is not specified
	# date = datetime.strftime(datetime.now(), "%Y-%m-%d")
	date = "1399-12-22"
	d = Date("shamsi", "greg", date, "روز پرستار")
	print(d.get_occasion_date())


def main():
	# All the time formats are in "YYYY-MM-DD HH:MM" or "YYYY-MM-DD"
	# and THEY SHOULD BE GREGORIAN except for date
	test_time()
	test_weather()
	test_rel_time()
	test_date()


if __name__ == '__main__':
	main()
