import requests
from bs4 import BeautifulSoup

from APIs.utility import *

DATE_CODE = {
	"shamsi": 1065,
	"gregorian": 1033,
	"hijri": 1025
}

CAL_TYPE_CODE = {
	"shamsi": 0,
	"gregorian": 1,
	"hijri": 2
}


class Date:
	def __init__(self, base_cal_type: str, target_cal_type: str, date: str,
	             occasion: str = ""):
		self.base_cal_type = base_cal_type
		self.target_cal_type = target_cal_type
		self.y, self.m, self.d = split_date(date)
		self.occasion = occasion
	
	def get_occasion_date(self):
		df = pd.read_csv("../shamsi_events.csv", encoding="utf-8")
		temp = df[(df["event"] == self.occasion)]
		ans = temp[temp["year"] == self.y].iloc[0]
		date = datetime(year=ans["year"],
		                month=ans["month"],
		                day=ans["day"]).strftime("%Y-%m-%d")
		return self.convert_date(date)
	
	def convert_date(self, date: str) -> str:
		y, m, d = split_date(date)
		resp = requests.get(f"https://www.time.ir/?"
		                    f"convertyear={y}&"
		                    f"convertmonth={m}&"
		                    f"convertday={d}&"
		                    f"convertlcid={CAL_TYPE_CODE[self.base_cal_type]}")
		if resp.status_code / 100 != 2:
			raise RuntimeError(
				f"Error {resp.status_code} while getting the page")
		
		soup = BeautifulSoup(resp.text, "html.parser")
		times = [soup.select(
			"#ctl00_cphMiddle_Sampa_Web_View_TimeUI_DateConvert00cphMiddle_3733_lblFirstDateNumeral")[
			         0].text,
		         soup.select(
			         "#ctl00_cphMiddle_Sampa_Web_View_TimeUI_DateConvert00cphMiddle_3733_lblSecondDateNumeral")[
			         0].text,
		         soup.select(
			         "#ctl00_cphMiddle_Sampa_Web_View_TimeUI_DateConvert00cphMiddle_3733_lblThirdDateNumeral")[
			         0].text]
		
		if self.base_cal_type == "gregorian":
			if self.target_cal_type == "shamsi":
				return times[1]
			elif self.target_cal_type == "hijri":
				return times[2]
		
		if self.base_cal_type == "shamsi":
			if self.target_cal_type == "gregorian":
				return times[1]
			elif self.target_cal_type == "hijri":
				return times[2]
		
		if self.base_cal_type == "hijri":
			if self.target_cal_type == "shamsi":
				return times[1]
			elif self.target_cal_type == "gregorian":
				return times[2]
		
		return "Not Found!"
