#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/11 16:54
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : __init__.py.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :

from ys_service.db_service.mysql_service import MysqlService
from ys_service.db_service.mongo_service import MongoService
from ys_service.db_service.redis_service import RedisService
from ys_service.db_service.sqlserver_service import SqlServerService


class DBService(object):

    def __init__(self):
        # 三种连接对象
        self.mysql_client = MysqlService()
        self.mongo_client = MongoService()
        self.redis_client = RedisService()
        self.sql_server_client = SqlServerService()
