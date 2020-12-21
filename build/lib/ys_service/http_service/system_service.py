#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/22 9:57
# @Author  : wiken
# @Site    : 
# @File    : system_service.py
# @Software: PyCharm
# @Desc    :

from datetime import datetime
import requests


BASE_URL = "http://192.168.0.100:5000"


def now():
    url = BASE_URL + "/api/System/GetServerInfo"
    res = requests.get(url)
    return parse_time(res.json())


def parse_time(time_dic):
    if time_dic.get("isSuccess"):
        _time = time_dic.get("data", {}).get("serverTime")
        _time = _time[:19]
        a = datetime.strptime(_time, "%Y-%m-%dT%H:%M:%S")
        return a
    else:
        return None

if __name__ == '__main__':
    print(now())