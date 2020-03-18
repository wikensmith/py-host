#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/12 15:21
# @Author  : wiken
# @Site    : 
# @File    : _http.py
# @Software: PyCharm
# @Desc    :


import requests


class _HTTP(object):

    def __init__(self):
        self.base_url = "http://192.168.0.100:5000"
        self.request = requests
