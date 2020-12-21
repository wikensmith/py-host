#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/14 16:06
# @Author  : wiken
# @Site    : 
# @File    : reservation_service.py
# @Software: PyCharm
# @Desc    :
from ys_service.http_service.utils import *
from ys_service.http_service._http import _HTTP


class CreateReservation(object):
    """
    创建预约服务类
    """

    @property
    def create(self):
        return ReservationService


class ReservationService(_HTTP):
    """
    本类实现队列的预约操作
    """
    def check_in(self, data):
        url = self.base_url + "/api/Reservation/CheckIn"
        res = self.request.post(url, json=data)

        return check_http_response(res)

    def query(self, data):
        url = self.base_url + "/api/Reservation/Query"
        res = self.request.post(url, json=data)

        return check_http_response(res)

    def cancel(self, data):
        url = self.base_url + "/api/Reservation/Cancel"
        res = self.request.post(url, json=data)

        return check_http_response(res)
