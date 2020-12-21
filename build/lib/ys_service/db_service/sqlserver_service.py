#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/14 9:51
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : sqlserver_service.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :

import pymssql
from ys_service.db_service.base_service import BaseDB

DEFAULT_SQL_SERVER_HOST = ""
DEFAULT_SQL_SERVER_USERNAME = ""
DEFAULT_SQL_SERVER_PASSWORD = ""
DEFAULT_SQL_SERVER_DB = ""


class SqlServerService(BaseDB):

    def connect(self, host=None, username=None, password=None, db=None):
        """
        创建连接对象，并返回对应游标
        :param host: mysql服务器地址
        :param username: 用户名
        :param password: 密码
        :param db: 数据库
        :return: 游标
        """
        _host = host if host else DEFAULT_SQL_SERVER_HOST or None
        _username = username if username else DEFAULT_SQL_SERVER_USERNAME or None
        _password = password if password else DEFAULT_SQL_SERVER_PASSWORD or None
        _db = db if db else DEFAULT_SQL_SERVER_DB or None
        # 获取数据库连接参数的hash值, 作为连接对象的键
        hash_value = self.get_hash(_host, _username, _password, _db)
        if not self.is_in_map(hash_value):
            conn = pymssql.connect(
                server=_host, user=_username, password=_password, database=_db
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
