from datetime import datetime
from typing import Tuple

import pandas as pd


def get_english_names(city: str) -> Tuple[str, str]:
	# df = pd.read_csv("fa_cities_final2.csv", encoding="utf-8")
	# print(df[df["city-fa"] == city])
	# eng_city = df[df["city-fa"] == city].iloc[0]["city"]
	
	df = pd.read_csv("cities15000.txt", usecols=[1, 2, 3, 8, 14], sep='\t',
	                 encoding="utf-8", header=None)
	res = df[df[3].str.contains(city) == True]
	target_row = res.sort_values(14, ascending=False).iloc[0]
	eng_city = target_row[2]
	cc = target_row[8]
	
	df = pd.read_csv("IP2LOCATION-COUNTRY-MULTILINGUAL.CSV", encoding="utf-8",
	                 header=None, skiprows=3736, nrows=249)
	eng_country = df[df[2] == cc].iloc[0][5]
	return eng_city, eng_country


def get_lat_lon(eng_city: str) -> Tuple[float, float]:
	df = pd.read_csv("cities15000.txt", usecols=[2, 4, 5, 14], sep='\t', encoding="utf-8", header=None)
	res = df[df[2].str.contains(eng_city) == True]
	target_row = res.sort_values(14, ascending=False).iloc[0]
	return round(target_row[4], 2), round(target_row[5], 2)


def split_date(date: str) -> Tuple[str, ...]:
	return tuple(date.split('-'))


# def split_datetime(dt: str) -> Tuple[str, ...]:
# 	dt_split = dt.split()
# 	date = tuple(split_date(dt_split[0]))
# 	time = ("12", "00") if len(dt_split) == 1 else tuple(dt_split[1].split(':'))
# 	return date + time

def parse_datetime(dt: str) -> int:
	temp = dt
	if len(dt.split()) == 1:
		temp += " 12:00"
	return int(datetime.timestamp(datetime.strptime(temp, "%Y-%m-%d %H:%M")))
