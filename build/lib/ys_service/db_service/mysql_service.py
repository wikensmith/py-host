#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/11 16:54
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : mysql.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :

import pymysql
from ys_service.db_service.base_service import BaseDB

DEFAULT_MYSQL_HOST = ""
DEFAULT_MYSQL_PORT = ""
DEFAULT_MYSQL_USERNAME = ""
DEFAULT_MYSQL_PASSWORD = ""
DEFAULT_MYSQL_DB = ""
DEFAULT_MYSQL_CHARSET = "utf8mb4"


class MysqlService(BaseDB):

    def connect(self, host=None, port=None, username=None, password=None, db=None, charset=None):
        """
        创建连接对象，并返回对应游标
        :param host: mysql服务器地址
        :param port: mysql服务端口
        :param username: 用户名
        :param password: 密码
        :param db: 数据库
        :param charset: 编码
        :param uri: 编码
        :return: 游标
        """
        _host = host if host else DEFAULT_MYSQL_HOST or None
        _port = port if port else DEFAULT_MYSQL_PORT or None
        _username = username if username else DEFAULT_MYSQL_USERNAME or None
        _password = password if password else DEFAULT_MYSQL_PASSWORD or None
        _db = db if db else DEFAULT_MYSQL_DB or None
        _charset = charset if charset else DEFAULT_MYSQL_CHARSET or None
        # 获取数据库连接参数的hash值, 作为连接对象的键
        hash_value = self.get_hash(_host, _port, _username, _password, _db, _charset)
        if not self.is_in_map(hash_value):
            conn = pymysql.Connect(
                host=_host, port=_port,
                user=_username, password=_password,
                database=_db, charset=_charset
            )
            self.add_to_map(hash_value, conn)

        return self.get_cursor(hash_value)

    def get_cursor(self, hash_value):
        """
        获取游标对象
        :param hash_value:
        :return:
        """

        return self.connect_map[hash_value].cursor()
