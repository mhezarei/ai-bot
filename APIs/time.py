from datetime import datetime
from bs4 import BeautifulSoup
import requests
from APIs.utility import get_english_names


class Time:
	def __init__(self, city: str):
		self.city, self.country = get_english_names(city)
		self.base_url = "https://www.timeanddate.com/worldclock/?query="
		self.url = ""
	
	def send_request(self):
		url = self.base_url + '+'.join([x for x in self.city.split()])
		self.url = url
		txt = requests.get(url).text
		soup = BeautifulSoup(txt, "html.parser")
		listing_select = soup.select("#p0")
		page_select = soup.select("#ct")
		if listing_select:
			return listing_select[0].text.split()[1]
		elif page_select:
			return page_select[0].text[:-3]
		else:
			return datetime.now().strftime("%H:%M")
