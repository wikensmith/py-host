#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/19 9:53
# @Author  : wiken
# @Site    : 
# @File    : context_attach_data_server.py
# @Software: PyCharm
# @Desc    : 对mongo数据库执行附加操作
from ys_service.http_service.utils import *


class ContextAttachDataServer(object):

    def __init__(self, handler, message_id=""):
        self.message_id = message_id
        self.attach_data_handler = handler  # 附加数据对象

    def __setitem__(self, key, value):
        """
        设置attach data的属性值
        :param key: 键名
        :param value: 值
        :return:
        """
        props = {key: value}
        data_type = "YS_Hosted"
        data_id = self.message_id

        response = self.attach_data_handler.set(props, data_type=data_type, data_id=data_id)

        print(check_http_response(response))

    def append(self, data):
        """
        向mongo数据库的data_type, data_id 中的attach_list追加数据。
        :param data: 数据, 字典格式{key: value}。
        :return: 操作结果, dict类型。
        """
        return self.attach_data_handler.append(
            data,
            data_type="YS_Hosted",
            data_id=self.message_id
        )

    def get_all(self):
        """
        通过 message_id 查询所有的属性值和attach_list的值。
        :return: 查询结果, dict类型。
        """
        return self.attach_data_handler.get_all(data_type="YS_Hosted", data_id=self.message_id)
