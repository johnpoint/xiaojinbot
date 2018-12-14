#!/bin/python3

import requests
import json

def get_url(key):
    r = requests.get('https://cast.jjldbk.com/api/series/' + key).text
    num = r.count('.')
    if r.find("error_code") == -1 :
        r = json.loads(r)
        return num,r
    else:
        return 0,404
