import requests
from APIs.utility import get_english_names, split_date

REL_TIME_CONVERSION = {
	"امساک": "Imsak",
	"اذان صبح": "Fajr",
	"طلوع آفتاب": "Sunrise",
	"اذان ظهر": "Dhuhr",
	"اذان عصر": "Asr",
	"غروب آفتاب": "Sunset",
	"اذان مغرب": "Maghrib",
	"اذان عشا": "Isha",
	"نیمه‌شب شرعی": "Midnight",
	"نیمه شب شرعی": "Midnight"
}


class ReligiousTime:
	def __init__(self, rel_time: str, city: str, date: str):
		self.rel_time = rel_time
		self.city, self.country = get_english_names(city)
		self.method = '2'
		self.year, self.month, self.day = split_date(date)
		self.base_url = "http://api.aladhan.com/v1/calendarByCity"
		self.url = ""
	
	def send_request(self) -> dict:
		# Gives us the religious timings
		url = self.base_url + '?'
		temp = self.__dict__.copy()
		temp.pop("rel_time")
		url += '&'.join([f"{i[0]}={i[1]}" for i in temp.items()])
		self.url = url
		resp = requests.get(url)
		return resp.json()["data"][int(self.day) - 1]["timings"]
	
	def get_rel_timing(self) -> str:
		# Returns the specified timing
		timings = self.send_request()
		return timings[REL_TIME_CONVERSION[self.rel_time]].split()[0]
