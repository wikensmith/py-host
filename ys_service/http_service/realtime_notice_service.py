#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/14 16:32
# @Author  : wiken
# @Site    : 
# @File    : realtime_notice.py
# @Software: PyCharm
# @Desc    :
from ys_service.http_service.utils import *
from ys_service.http_service._http import _HTTP


class CreateRealtimeNoticeService(object):
    """
        创建实时消息服务
    """
    @property
    def create(self):
        return RealtimeNoticeService


class RealtimeNoticeService(_HTTP):
    """
        实时消息
    """
    def new_notice(self, data):
        url = self.base_url + "/api/RealtimeNotice/NewNotice"
        response = self.request.post(url, json=data)

        return check_http_response(response)
