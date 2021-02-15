import pandas as pd
import datetime
import os


def find_events(sentence, dates, all_events, all_event_keys):
    events = []
    event_keys = []
    p = os.path.dirname(os.path.abspath(__file__))
    if "مناسبت" in sentence:
        event_year = dates[0].split('-')[0]
        event_month = dates[0].split('-')[1]
        event_day = dates[0].split('-')[2]
        new_dates = dates
        url1 = os.path.join(p, event_year + ".csv")
        df2 = pd.read_csv(url1)
        for idx, row in df2.iterrows():
            if str(row["month"]) == event_month and str(row["day"]) == str(event_day):
                events.append(row["event"])
                break
    else:
        for i in range(len(all_events)):
            if all_events[i] in sentence or all_event_keys[i] in sentence:
                events.append(all_events[i])
                event_keys.append(all_event_keys[i])
        new_dates = []
        if len(events) > 0 and len(dates) > 0:
            year = dates[0].split('-')[0]
            url1 = os.path.join(p, year + ".csv")
            df2 = pd.read_csv(url1)

            for idx, row in df2.iterrows():
                if row["event"] == event_keys[0]:
                    date = datetime.datetime(row['year'], row['month'], row['day'])
                    new_dates.append(date.strftime('%Y-%m-%d'))
                    break
        if len(new_dates) == 0:
            new_dates = dates
    print("events : " + str(events))

    return events, new_dates
