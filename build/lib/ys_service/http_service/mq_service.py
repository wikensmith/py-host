#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/14 11:22
# @Author  : wiken
# @Site    : 
# @File    : mq_service.py
# @Software: PyCharm
# @Desc    :
import time
from typing import Optional, Any

from ys_service.http_service._http import _HTTP
from ys_service.http_service.utils import *


class MQService(_HTTP):
    """
    本服务实现对队列消息的操作
    """
    def push_msg(self, data):
        """
        发送消息到队列
        :param data:
        :return:
        """
        url = self.base_url + "/api/MQ/PushMessage"
        res = self.request.post(url, json=data)

        return check_http_response(res)

    def pop_msg(self, data):
        """
        删除队头的一条消息并返回该条消息
        :param data:
        :return:
        """
        url = self.base_url + "/api/MQ/PopMessage"
        res = self.request.post(url, json=data)

        return check_http_response(res)

    def send_response(self, data):
        """
        向队列发送一条消息
        :param data:
        :return: info
        """
        url = self.base_url + "/api/MQ/SendResponse"
        res = self.request.post(url, json=data)
        return check_http_response(res)

    def send_request(self, data):
        """
        向指定队列发送一条,并等待回复
        :param data:
        :return: response
        """
        url = self.base_url + "/api/MQ/SendRequest"
        res = self.request.post(url, json=data)

        return check_http_response(res)

    def get_response(self, correlation_id, routing_key=None):
        """
        通过 correlationd_id 获取 send_response 的结果
        :param correlation_id:
        :param routing_key:
        :return:
        """
        param = {
            "correlationId": correlation_id,
            "routingKey": routing_key
        }

        url = self.base_url + "/api/MQ/GetResponse"
        res = self.request.get(url, params=param)

        return check_http_response(res)

    def wait_response(self, data=None, timeout=60, correlation_id=None):
        """
        发送push_msg 并循环获取数据结果，超时结果, 超时时间不能小于3s
        使用方法：
        1、传入参数data为字典类型， correlation_id = None 时， 为先push msg 再循环等待接收内容
        2、当不传data， 只传入correlation_id 的时候，只进行针对该 id 的循环接收内容操作
        :param correlation_id:
        :param data: dict
        :param timeout: 最长等待时候
        :return: {"is_success": True, "status_code": 200,"message": "", "data":data}
        """

        def wait_for_response():
            while True:
                time.sleep(1)
                time_passed = int(time.time() - start_time)
                print(time_passed)

                if time_passed >= timeout:
                    return return_msg(is_success=False, msg="获取超时")
                if time_passed % 3 == 0:
                    # 返回[] 或数据dict
                    result_dic = self.get_response(correlation_id=correlation_id)
                    if result_dic:
                        return return_msg(is_success=True, data=result_dic)

        start_time = int(time.time())

        if not correlation_id:
            correlation_id = hash(time.time())
            data["correlationId"] = correlation_id
            res = self.push_msg(data)
            if res.get("isSuccess"):
                return wait_for_response()
            else:
                return return_msg(is_success=False,
                                  msg="push msg 失败, status_code:{}".format(res.status_code))
        else:
            return wait_for_response()


class CreateMQ(object):

    @staticmethod
    def create():
        """
        创建mq_service 对象
        :return:
        """
        return MQService()
