import pandas as pd
import datetime
import os


def find_events(sentence, dates):
    p = os.path.dirname(os.path.abspath(__file__))
    url1 = os.path.join(p, "find important events.csv")
    df1 = pd.read_csv(url1)
    important_events = df1['event']
    important_events_key = df1['event_key']
    event_keys = []
    events = []
    if "مناسبت" in sentence:
        event_year = dates[0].split('-')[0]
        event_month = dates[0].split('-')[1]
        event_day = dates[0].split('-')[2]
        new_dates = dates
        url1 = os.path.join(p, event_year + ".csv")
        df2 = pd.read_csv(url1)
        print(event_year)
        print(event_month)
        print(event_day)
        for idx, row in df2.iterrows():
            if str(row["month"]) == event_month and str(row["day"]) == str(event_day):
                print(row["event"])
                events.append(row["event"])
                break
    else:
        for i in range(len(important_events)):
            if important_events_key[i] in sentence:
                events.append(important_events[i])
                event_keys.append(important_events_key[i])
            elif important_events[i] in sentence:
                events.append(important_events[i])
                event_keys.append(important_events_key[i])
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
