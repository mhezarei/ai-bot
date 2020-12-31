import pandas as pd
import datetime


def find_events(sentence, dates):
    url1 = "Data/events/important events.csv"
    df1 = pd.read_csv(url1)
    important_events = df1['event']
    important_events_key = df1['event_key']

    events = []
    for i in range(len(important_events)):
        if important_events_key[i] in sentence:
            events.append(important_events_key[i])
        elif important_events[i] in sentence:
            events.append(important_events_key[i])
    new_dates = []
    if len(events) > 0 and len(dates)>0:
        year = dates[0].split('-')[0]
        url1 = "Data/events/Shamsi/" + year + ".csv"
        df2 = pd.read_csv(url1)

        for idx, row in df2.iterrows():
            if row["event"] == events[0]:
                date = datetime.datetime(row['year'], row['month'], row['day'])
                new_dates.append(date.strftime('%Y-%m-%d'))
                break
    if len(new_dates) == 0:
        new_dates = dates
    return events, new_dates
