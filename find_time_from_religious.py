from religious_time import ReligiousTime
from utility import convert_date


def find_time_from_religious(answer):
    results = []
    urls = []
    for religious_time in answer["religious_time"]:
        greg_date = convert_date(answer["date"][0], "shamsi",
                                 "greg")
        rl = ReligiousTime(religious_time, answer["city"][0],
                           greg_date)
        results.append(rl.get_rel_timing())
        urls.append(rl.url)
    return results, urls
