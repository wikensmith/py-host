#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/22 15:48
# @Author  : wiken
# @Site    : 
# @File    : ys_requests.py
# @Software: PyCharm
# @Desc    :
import requests
from datetime import datetime, timedelta
from ys_service.http_service.system_service import now


class YsRequests(object):
    def __init__(self, context):
        self.session = requests.Session()
        self.start_time = now()
        self._deadline = context.get_header("deadline")
        self.set_deadline()

    def set_deadline(self):
        if self._deadline:
            self._deadline = datetime.strptime(self._deadline, "%Y-%m-%d %H:%M:%S")

    @classmethod
    def create(cls, context):
        """
        创建ys_requests 实例
        :param context:
        :return: 实例对象
        """
        return cls(context)

    def get(self, *args, **kwargs):
        return self.requests("get", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.requests("post", *args, **kwargs)

    def requests(self, *args, **kwargs):
        timeout = kwargs.setdefault("timeout", 30)
        self.is_timeout(timeout)
        return self.session.request(*args, **kwargs)

    def is_timeout(self, timeout):
        """
        从队列消息中得到到期时间，如果下一次请求超时后还不到期则执返回True
        :param timeout:
        :return: bool
        """
        if self._deadline:
            if self._deadline - now() < timedelta(seconds=timeout):
                raise TimeoutError("超时, 已熔断")


if __name__ == "__main__":
    pass
