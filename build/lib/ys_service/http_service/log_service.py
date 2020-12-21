#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/12 15:20
# @Author  : wiken
# @Site    : 
# @File    : log_service.py
# @Software: PyCharm
# @Desc    :
import time
from ys_service.http_service._http import _HTTP


class LogService(_HTTP):
    def __init__(self, application_property, trace_property):
        super(LogService, self).__init__()

        self.application_property = application_property
        self.trace_property = trace_property

    def send_log(self, message, data_property=None, level="info"):
        """
        send log to log_center
        :param data_property:
        :param message:
        :param level: The level of message.
        :return: response
        """

        data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": level,
            "message": message,
            "properties": {
                "applicationProperty": self.application_property,
                "dataProperty": data_property,
                "traceProperty": self.trace_property
            }
        }

        url = self.base_url + "/api/LogCenter/NewLog"

        res = self.request.post(url, json=data)
        print("res code", res.status_code)
        return res


class LogCreate(object):

    @staticmethod
    def create(application_properties=None, trace_property=None):
        """
        传入基础数据, 数据详情请见：http://192.168.0.100:5000/swagger/index.html
        :param application_properties:
        :param trace_property:
        :return: log_service 对象
        """

        return LogService(application_properties, trace_property)
