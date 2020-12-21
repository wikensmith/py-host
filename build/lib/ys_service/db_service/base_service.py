#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/11 17:38
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : base.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :

from abc import ABC, abstractmethod


class BaseDB(ABC):

    def __init__(self):
        self.connect_map = {}

    @abstractmethod
    def connect(self, **kwargs):
        """
        创建数据库连接
        :param kwargs: 连接数据库的参数
        :return:
        """
        pass

    @staticmethod
    def get_hash(*args):
        """
        获取args参数拼接字符串的hash值
        :param s:
        :return:
        """
        object_name = __class__.__name__
        a = [str(i) for i in args]
        a.append(object_name)
        return hash("".join(a))

    def is_in_map(self, hash_value):
        """
        判断hash_value的连接是否存在
        :param hash_value: 哈希值
        :return: 存在返回True， 不存在返回False
        """
        return True if self.connect_map.get(hash_value) else False

    def add_to_map(self, hash_value, conn):
        """
        把连接添加到map对象中,
        :param hash_value:
        :param conn:
        :return:
        """
        self.connect_map[hash_value] = conn

    def close(self):
        """
        关闭连接
        :return:
        """
        for conn in self.connect_map.values():
            conn.close()
