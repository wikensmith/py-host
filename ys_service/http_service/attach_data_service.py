#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/15 11:57
# @Author  : wiken
# @Site    : 
# @File    : attach_data_service.py
# @Software: PyCharm
# @Desc    : 实现通过data_id 和data_type 把数据通过键值对的形式或附加的存储到数据库中，实现新加、追加、查询、等操作。返回数据类统一为json格式
import json
import datetime

from ys_service.http_service.utils import *
from ys_service.http_service._http import _HTTP


class AttachDataService(_HTTP):
    def get(self, data_type, data_id, timeout=30, props=None):
        """
        通过props获取attach 中的数据
        :param data_type: 数据类型（如:YATP）
        :param data_id: 数据唯一id
        :param timeout: 超时时间
        :param props: 需要获取值的健的列表，
        :return: 得到的数据， dict类型
        """

        url = self.base_url + "/api/MQ/SendRequest"

        data = {
            "timeoutSeconds": timeout,
            "exchangeName": "system.request",
            "routingKey": "system.request.attach_data",
            "requestHeaders": {
                "message_type": "get_prop" if props else "get_props",
                "data_type": data_type,
                "data_id": data_id
            },
            "requestData": ""}

        response = self.request.post(url=url, json=data)

        return check_http_response(response)

    def set(self, props, data_type, data_id, timeout=30):
        """
        根据id设置属性值
        :param timeout:
        :param props: 需要设置的属性值
        :param str data_type: 数据类型（如:YATP）
        :param str data_id: 数据唯一id
        :return: 设置是否成功返回值
        """

        url = self.base_url + "/api/MQ/SendRequest"

        data = {
          "timeoutSeconds": timeout,
          "exchangeName": "system.request",
          "routingKey": "system.request.attach_data",
          "requestHeaders": {
            "message_type": "set_prop",
            "data_type": data_type,
            "data_id": data_id
          },
          "requestData": json.dumps(props),
          "executionTime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[0:23] + "Z"
        }
        response = self.request.post(url, json=data)

        return check_http_response(response)

    def append(self, data, data_type, data_id):
        """
        在属性后附加数据, 附加的数据以字典的格式传入，在数据库中存在attachList 中，
        可以使用 get_all 方法获取。
        :param data: 需要附加的内容， 可以是任何形式的值。
        :param str data_type: 数据类型（如:YATP）
        :param str data_id: 数据唯一id
        :return: 设置是否成功返回值
        """

        url = self.base_url + "/api/MQ/SendRequest"

        data = {
            "exchangeName": "system.request", "routingKey": "system.request.attach_data",
            "requestHeaders": {
                "message_type": "append_data",
                "data_type": data_type,
                "data_id": data_id
            },
            "requestData": json.dumps(data),
            # "requestData": data,
            "executionTime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[0:23] + "Z"}

        response = self.request.post(url, json=data)
        return check_http_response(response)

    def get_all(self, data_type, data_id, timeout=30):
        """
        根据data_type 和 data_id 获取所有的prop值和 attachList 中的值
        :param str data_type: 数据类型（如:YATP）
        :param str data_id: 数据唯一id
        :param timeout: 超时时间
        :return: 设置是否成功返回值
        """

        url = self.base_url + "/api/MQ/SendRequest"
        data = {
          "timeoutSeconds": timeout,
          "exchangeName": "system.request",
          "routingKey": "system.request.attach_data",
          "requestHeaders": {
            "message_type": "query_data",
            "data_type": data_type,
            "data_id": data_id
          },
          "requestData": ""
        }
        response = self.request.post(url=url, json=data)
        dic = check_http_response(response)

        len_of_attach_lst = len(dic.get("Data", {}).get("AttachList"))
        for i in range(len_of_attach_lst):
            dic["Data"]["AttachList"][i]["AttachTime"] = convert_time(
                dic.get("Data", {}).get("AttachList")[i].get("AttachTime")
            )
        return dic


class CreateAttachDataService(object):
    @staticmethod
    def create():
        return AttachDataService()
