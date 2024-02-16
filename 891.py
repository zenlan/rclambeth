#!/usr/bin/ python3

import requests
import json

def fetch_text(url):
    r = requests.get(url)
    if r.status_code == 200:
        foo = json.loads(r.content)
        json.dump(foo, open('891.json', 'w'))
        open('891.js', 'w').write("data=" + json.dumps(foo))

fetch_text('https://restarters.net/api/v2/groups/891')