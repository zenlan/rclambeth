#!/usr/bin/ python3

import requests
import json
import polars as pl
import funcs

# https://github.com/TheRestartProject/restarters.net/blob/develop/routes/api.php

def fetch_group():
    url = "https://restarters.net/api/v2/groups/891"
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        json.dump(data, open('891.json', 'w'), indent=4, ensure_ascii=False)
        open('891.js', 'w').write("response=" + json.dumps(data, indent=4, ensure_ascii=False))


def fetch_events():
    url = "https://restarters.net/api/v2/groups/891/events"
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        json.dump(data, open('out/891_events.json', 'w'), indent=4, ensure_ascii=False)
    return data

def read_events():

    schema = {"id" : pl.Int64, "start" : pl.String, "end" : pl.String}
    df = pl.DataFrame(schema=schema)
    data = json.load(open('out/891_events.json', 'r'))
    for i in range(0,len(data["data"])):
        foo = data["data"][i]
        tmp = pl.DataFrame(data={"id" : foo["id"], "start" : foo["start"], "end" : foo["end"]}, schema=schema)
        df = pl.concat([df, tmp])
    df.write_csv("out/891_events.csv")
    return df


def fetch_event(event_id):
    url = f"https://restarters.net/api/v2/events/{event_id}"
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        json.dump(data, open(f"out/891_event_{event_id}.json", 'w'), indent=4, ensure_ascii=False)


if __name__ == "__main__":

    logger = funcs.init_logger()

    fetch_group()

    # events = fetch_events()

    # df_evts = read_events()

    # for evt in df_evts.iter_rows(named=True):
    #     id = evt["id"]
    #     fetch_event(id)