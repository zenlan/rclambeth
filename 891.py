#!/usr/bin/ python3

import requests
import json

def fetch_text(url):
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        json.dump(data, open('891.json', 'w'), indent=4, ensure_ascii=False)
        open('891.js', 'w').write("response=" + json.dumps(data, indent=4, ensure_ascii=False))

fetch_text('https://restarters.net/api/v2/groups/891')