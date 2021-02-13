from religious_time import ReligiousTime
from utility import convert_date


def find_time_from_religious(answer):
    greg_date = convert_date(answer["date"][0], "shamsi",
                             "greg")
    rl = ReligiousTime(answer["religious_time"][0], answer["city"][0],
                       greg_date)
    res = rl.get_rel_timing()
    print("res", res)
    return str(res), rl.url
