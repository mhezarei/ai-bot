import os

import pandas as pd


def find_events_in_sentence(sentence):
    p = os.path.dirname(os.path.abspath(__file__))
    url1 = os.path.join(p, "find important events.csv")
    df1 = pd.read_csv(url1)
    important_events = df1['event']
    important_events_key = df1['event_key']
    events = []
    event_keys = []
    for i in range(len(important_events)):
        if important_events_key[i] in sentence:
            events.append(important_events[i])
            event_keys.append(important_events_key[i])
        elif important_events[i] in sentence:
            events.append(important_events[i])
            event_keys.append(important_events_key[i])
    more_events = {
        "عاشورا": "عاشورای حسینی",
        "تاسوعا": "تاسوعای حسینی"
    }
    for key in more_events.keys():
        if not more_events[key] in events and key in sentence:
            events.append(more_events[key])
            event_keys.append(more_events[key])
    #TODO
    print("all events : " + str(events))
    return events, event_keys
