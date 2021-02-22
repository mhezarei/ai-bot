import os
from datetime import datetime
from typing import Tuple

import jdatetime
import pandas as pd
from hijri_converter import convert


def get_english_names(city: str) -> Tuple[str, str]:
    p = os.path.dirname(os.path.abspath(__file__))
    f = os.path.join(p, "cities15000.txt")
    df = pd.read_csv(f,
                     usecols=[1, 2, 3, 8, 14], sep='\t',
                     encoding="utf-8", header=None)
    res = df[df[3].str.contains(city) == True]
    target_row = res.sort_values(14, ascending=False).iloc[0]
    eng_city = target_row[2]
    cc = target_row[8]

    p = os.path.dirname(os.path.abspath(__file__))
    f = os.path.join(p, "IP2LOCATION-COUNTRY-MULTILINGUAL.CSV")
    df = pd.read_csv(f,
                     encoding="utf-8",
                     header=None, skiprows=3736, nrows=249)
    eng_country = df[df[2] == cc].iloc[0][5]
    return eng_city, eng_country


def get_lat_lon(eng_city: str) -> Tuple[float, float]:
    p = os.path.dirname(os.path.abspath(__file__))
    f = os.path.join(p, "cities15000.txt")
    df = pd.read_csv(f, usecols=[2, 4, 5, 14],
                     sep='\t',
                     encoding="utf-8", header=None)
    res = df[df[2].str.contains(eng_city) == True]
    target_row = res.sort_values(14, ascending=False).iloc[0]
    return round(target_row[4], 2), round(target_row[5], 2)


def split_date(date: str) -> Tuple[str, ...]:
    return tuple(date.split('-'))


def convert_date(date: str, base: str, target: str) -> str:
    if base == target:
        return date
    if base == "shamsi":
        y, m, d = map(int, split_date(date))
        greg = str(jdatetime.date(year=y, month=m, day=d).togregorian())
        y, m, d = map(int, split_date(greg))
        hijri = str(convert.Gregorian(y, m, d).to_hijri())
        if target == "greg":
            return greg
        elif target == "hijri":
            return hijri
    elif base == "greg":
        y, m, d = map(int, split_date(date))
        shamsi = str(jdatetime.date(year=y, month=m, day=d).fromgregorian())
        hijri = str(convert.Gregorian(y, m, d).to_hijri())
        if target == "shamsi":
            return shamsi
        elif target == "hijri":
            return hijri
    elif base == "hijri":
        y, m, d = map(int, split_date(date))
        greg = str(convert.Hijri(y, m, d).to_gregorian())
        y, m, d = map(int, split_date(greg))
        shamsi = str(jdatetime.date(year=y, month=m, day=d).fromgregorian())
        if target == "greg":
            return greg
        elif target == "shamsi":
            return shamsi


def parse_datetime(dt: str) -> int:
    temp = dt
    if len(dt.split()) == 1:
        temp += " 12:00"
    return int(datetime.timestamp(datetime.strptime(temp, "%Y-%m-%d %H:%M")))
