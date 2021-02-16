
import requests
from utility import *


class Weather:
    def __init__(self, city: str, dt: str, current_dt: int, full_day: bool = False):
        self.city, self.country = get_english_names(city)
        self.lat, self.lon = get_lat_lon(self.city)
        self.dt = parse_datetime(dt)
        self.current_dt = current_dt
        self.current_url = "api.openweathermap.org/data/2.5/weather?appid=345d8217035c76f9bd352963c9f009a7&"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/onecall?appid=345d8217035c76f9bd352963c9f009a7&units=metric&exclude=alerts,minutely&"
        self.history_url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?appid=345d8217035c76f9bd352963c9f009a7&units=metric&"
        self.url = ""
        self.full = full_day

    def send_request(self):
        # if self.current_dt - self.dt >= 5 * 24 * 3600:
        # 	raise ValueError(
        # 		"The requested past time must be within the last 5 days!")
        # elif self.dt - self.current_dt >= 7 * 24 * 3600:
        # 	raise ValueError(
        # 		"The requested future time must be within the next 7 days!")

        if self.dt < self.current_dt:
            url = self.history_url + '&'.join(
                ["lat=" + str(self.lat), "lon=" + str(self.lon),
                 "dt=" + str(self.dt)])
            self.url = url
        else:
            url = self.forecast_url + '&'.join(
                ["lat=" + str(self.lat), "lon=" + str(self.lon)])
            self.url = url

        resp = requests.get(url)
        if resp.status_code / 100 != 2:
            raise RuntimeError(
                f"Error {resp.status_code} while getting the page")

        if self.full:
            return self.parse_full(resp.json())
        elif self.dt < self.current_dt:
            return self.parse_history(resp.json())
        else:
            return self.parse_future(resp.json())

    def parse_history(self, data) -> Tuple[str, str]:
        return self.extract_cond(data["current"])

    def parse_future(self, data) -> Tuple[str, str]:
        dt_utc = self.dt
        for h in data["hourly"]:
            if abs(dt_utc - h["dt"]) <= 1800:  # add and
                return self.extract_cond(h)
        for d in data["daily"]:
            if abs(dt_utc - d["dt"]) <= 12 * 3600:  # add and
                return self.extract_cond(d)
        return "", ""

    def extract_cond(self, pred: dict) -> Tuple[str, str]:
        # Return the temperature and weather condition code
        temp = pred["temp"] if isinstance(pred["temp"], float) else \
            pred["temp"]["day"]
        cond = pred["weather"][0]["main"].lower()
        cond_persian = -1
        if "cloud" in cond:
            cond_persian = "ابری"
        elif "rain" in cond:
            cond_persian = "بارانی"
        elif "clear" in cond:
            cond_persian = "آفتابی"
        elif "snow" in cond:
            cond_persian = "برفی"
        elif "storm" in cond:
            cond_persian = "طوفانی"
        return str(temp), cond_persian

    def parse_full(self, data) -> list:
        start_time = self.dt - 12 * 3600
        finish_time = start_time + (23 * 3600)
        print("start time : " + str(start_time) + " finish time : " + str(finish_time))
        temps = [float(t["temp"]) for t in data["hourly"] if start_time <= t["dt"] <= finish_time]
        minimum = 0.00
        maximum = 0.00
        for d in data["daily"]:
            if 24 * 3600 >= d["dt"] - (self.dt - 12 * 3600) >= 0:
                minimum = d["temp"]["min"]
                maximum = d["temp"]["max"]
                break
        print("temps : " + str(temps))
        if len(temps) == 0:
            mid = 0.00
        else:
            mid = round(sum(temps) / len(temps), 2)
        out = [round(minimum, 2), round(maximum, 2), mid]
        return out
