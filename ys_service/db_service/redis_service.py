
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/11 16:54
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : redis.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :
from redis import StrictRedis
from redis_lock import Lock
from ys_service.db_service.base_service import BaseDB

REDIS_DEFAULT_HOST = "localhost"
REDIS_DEFAULT_PORT = 6379
REDIS_DEFAULT_USERNAME = ""
REDIS_DEFAULT_PASSWORD = ""
REDIS_DEFAULT_DB = 0


class RedisService(BaseDB):

    def connect(self, host=None, port=None, password=None, db=None):
        """
        连接到redis
        :param host:
        :param port:
        :param password:
        :param db:
        :return:
        """
        _host = host if host else REDIS_DEFAULT_HOST or None
        _port = port if port else REDIS_DEFAULT_PORT or None
        _password = password if password else REDIS_DEFAULT_PASSWORD or None
        _db = db if db else REDIS_DEFAULT_DB or None
        hash_value = self.get_hash(_host, _port, _password, _db)
        if not self.is_in_map(hash_value):
            conn = YsRedis(host=_host, port=_port, password=_password, db=_db)
            self.add_to_map(hash_value, conn)

        return self.connect_map[hash_value]


class YsRedis(StrictRedis):

    def get_lock(self, lock_name, lock_ttl=None):
        """
                申请锁
                :param lock_name: lock的名字
                :param lock_ttl: 锁的生存时间, 单位为“秒”
                :return:
                """
        lock = YsLock(
            redis_client=self, name=lock_name, expire=lock_ttl
        )
        return lock


class YsLock(Lock):

    def __init__(self, redis_client, name, expire=None, id=None, auto_renewal=False, strict=True):
        super(YsLock, self).__init__(
            redis_client, name, expire=expire,
            id=id, auto_renewal=auto_renewal,
            strict=strict
        )
        self._name = "CSRedisClientLock:" + name
        self._signal = 'CSRedisClientLock-signal:' + name
