#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/14 16:33
# @Author  : wiken
# @Site    : 
# @File    : config_center.py
# @Software: PyCharm
# @Desc    :
from ys_service.http_service.utils import *
from ys_service.http_service._http import _HTTP


class CreateConfigCenterService(object):
    """
        创建配置中心服务
    """
    @property
    def create(self):
        return ConfigCenterService


class ConfigCenterService(_HTTP):
    """
    创建配置中心实例
    """
    def push(self, data):
        url = self.base_url + "/api/ConfigCenter/Push"
        response = self.request.post(url, data)

        return check_http_response(response)

    def active(self, data):
        url = self.base_url + "/api/ConfigCenter/Active"
        response = self.request.post(url, data)

        return check_http_response(response)

    def pull(self, data):
        url = self.base_url + "/api/ConfigCenter/Pull"
        response = self.request.post(url, data)

        return check_http_response(response)

    def fetch(self, data):
        url = self.base_url + "/api/ConfigCenter/Fetch"
        response = self.request.post(url, data)

        return check_http_response(response)
