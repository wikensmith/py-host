#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/11 16:54
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : mongo.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :
from decimal import Decimal
from bson.json_util import dumps, loads, ObjectId
from bson.decimal128 import Decimal128
from decimal import InvalidOperation
from pymongo import MongoClient
from pymongo.bulk import BulkOperationBuilder
from ys_service.db_service.base_service import BaseDB


DEFAULT_MONGO_HOST = ""
DEFAULT_MONGO_PORT = ""
DEFAULT_MONGO_USERNAME = ""
DEFAULT_MONGO_PASSWORD = ""
DEFAULT_MONGO_DB = ""


class MongoService(BaseDB):

    def connect(self, host=None, port=None, username=None, password=None, db=None):
        """
        获取mongo连接对象
        :param host:
        :param port:
        :param username:
        :param password:
        :param db:
        :return:
        """
        _host = host if host else DEFAULT_MONGO_HOST or None
        _port = port if port else DEFAULT_MONGO_PORT or None
        _username = username if username else DEFAULT_MONGO_USERNAME or None
        _password = password if password else DEFAULT_MONGO_PASSWORD or None
        _db = db if db else DEFAULT_MONGO_DB or None
        hash_value = self.get_hash(_host, _port, _username, _password, _db)
        # 如果不存在先创建连接
        if not self.is_in_map(hash_value):
            conn = MongoClient(host=_host, port=port, username=_username, password=_password)
            self.add_to_map(hash_value, conn)

        return self.get_db(hash_value, _db)

    def get_db(self, hash_value, db):
        """
        获取db对象
        :param hash_value:
        :param db:
        :return:
        """
        return self.connect_map[hash_value][db]

    def connect_ys(self, user, password, db):
        uri = f"mongodb://{user}:{password}@192.168.0.100:27017,192.168.0.100:27018/?replicaSet=rs0"

        hash_value = self.get_hash(uri)
        if not self.is_in_map(hash_value):
            conn = MongoClient(host=uri, replicaSet="rs0")
            self.add_to_map(hash_value, conn)
        return self.get_db(hash_value, db=db)

    @staticmethod
    def bulk(collection, ordered=True, passive_document_validation=False):
        """
        批量执行
        :param collection: 操作
        :param ordered: True所有命令将按顺序执行，并且第一个出错就会中止整个流程，False将按
                        任意顺序执行，可能是并行的，并且报告所有的操作完成后的错误。默认为True
        :param passive_document_validation:（可选）如果为True，则允许写入选择退出文档级别的验证。
                        默认值为 False。
        :return:
        """
        return BulkOperationBuilder(collection, ordered, passive_document_validation)

    @staticmethod
    def dumps(value):
        return dumps(value)

    @staticmethod
    def loads(value):
        return loads(value)

    @staticmethod
    def object_id(s):
        return ObjectId(s)

    @staticmethod
    def decimal128(s):
        """
        浮点数或者字符串转化为decimal128
        :param s:
        :return:
        """
        if isinstance(s, Decimal128):
            money = s
        else:
            try:
                money = Decimal128(s)
            except (ValueError, InvalidOperation):
                money = Decimal128("0")
        return Decimal128(money.to_decimal().quantize(Decimal("0.00")))
