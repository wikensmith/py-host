#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/20 9:48
# @Author  : wiken
# @Site    : 
# @File    : web_service_client.py
# @Software: PyCharm
# @Desc    :
from suds.client import Client


class CreateWebServiceClient(object):
    def create(self, url):
        client = Client(url)
        return client
