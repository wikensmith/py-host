#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/8 10:47
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : ys_hos.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :
import logging
from functools import partial
from typing import Optional
from retrying import retry
from pika.exceptions import AMQPError
from apscheduler.schedulers.blocking import BlockingScheduler
from ys_service.http_service.system_service import now
from ys_service.queue_service.block_service import BlockService
from ys_service.timing_service.timing_service import TimingService
from ys_service.service_provider import ServiceProvider

FLAG = """

$$$$$$$\ $$\     $$\ $$$$$$$$\ $$\   $$\  $$$$$$\  $$\   $$\       $$\   $$\  $$$$$$\   $$$$$$\ $$$$$$$$\ 
$$  __$$\\$$\   $$  |\__$$  __|$$ |  $$ |$$  __$$\ $$$\  $$ |      $$ |  $$ |$$  __$$\ $$  __$$\\__$$  __|
$$ |  $$ |\$$\ $$  /    $$ |   $$ |  $$ |$$ /  $$ |$$$$\ $$ |      $$ |  $$ |$$ /  $$ |$$ /  \__|  $$ |   
$$$$$$$  | \$$$$  /     $$ |   $$$$$$$$ |$$ |  $$ |$$ $$\$$ |      $$$$$$$$ |$$ |  $$ |\$$$$$$\    $$ |   
$$  ____/   \$$  /      $$ |   $$  __$$ |$$ |  $$ |$$ \$$$$ |      $$  __$$ |$$ |  $$ | \____$$\   $$ |   
$$ |         $$ |       $$ |   $$ |  $$ |$$ |  $$ |$$ |\$$$ |      $$ |  $$ |$$ |  $$ |$$\   $$ |  $$ |   
$$ |         $$ |       $$ |   $$ |  $$ | $$$$$$  |$$ | \$$ |      $$ |  $$ | $$$$$$  |\$$$$$$  |  $$ |   
\__|         \__|       \__|   \__|  \__| \______/ \__|  \__|      \__|  \__| \______/  \______/   \__|   

"""


class Host(object):
    """
    云上host
    """
    def __init__(
            self,
            username: str,
            password: str,
            host: str,
            port: int = 15672,
            heartbeat: int = 5,
            prefetch: int = 3,
            thread_num: Optional[int] = None,
            log_level: Optional[int] = logging.INFO,
            log_format: Optional[str] = None,
    ):
        # 队列服务

        self.queue_server = BlockService(
            username, password, host,
            port, heartbeat, prefetch, thread_num,
            log_level, log_format
        )
        # 定时服务
        self.time_server = TimingService()
        # 数据库等service提供者
        self.service = ServiceProvider()

    def register(self, queue_name, auto_ack=False, prefetch=3, **config_map):
        """
        注册队列名字
        :param queue_name: 队列名
        :param auto_ack: 是否自动回复
        :param prefetch: 流量数
        :param config_key: 配置中心的key
        :return:
        """
        def _inner(f):
            return self.queue_server.register(queue_name, auto_ack, prefetch, self.service, **config_map)(f)
        return _inner

    def timing(self, trigger, **kwargs):
        """
        注册定时时间
        :param trigger:
        :param kwargs:
        :return:
        """
        def _inner(f):
            _f = partial(f, service=self.service)
            return self.time_server.timing_server(trigger, **kwargs)(_f)
        return _inner

    @property
    def queue_map(self):
        """
        获取queue_map
        :return:
        """
        return self.queue_server.queue_map

    def start(self):

        print(FLAG)
        self.start_only_timing()
        self.start_only_queue()

    @retry(wait_fixed=10 * 1000, retry_on_exception=lambda exception: isinstance(exception, AMQPError))
    def start_only_queue(self):
        BlockService.start(self.queue_server)

    def start_only_timing(self):
        if not self.queue_map:
            self.time_server.scheduler = BlockingScheduler()
        TimingService.start(self.time_server)
        # BlockService.start(self.queue_server)

    @staticmethod
    def now():
        return now()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        for _, v in self.service.mongo_client.connect_map.items():
            v.close()

        for _, v in self.service.mysql_client.connect_map.items():
            v.close()

        for _, v in self.service.redis_client.connect_map.items():
            v.close()

        for _, v in self.service.sql_server_client.connect_map.items():
            v.close()

        self.queue_server.connection.close()
        print("host网络连接关闭完毕")
