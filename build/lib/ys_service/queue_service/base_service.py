#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/5 13:38
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : server.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :

import logging
from typing import Optional, Callable
from ys_service.queue_service.queue import Queue
from ys_service.queue_service.context import Context
from threading import Lock


class BaseService(object):

    DEFAULT_LOG_FORMAT = "%(levelname) -5s %(asctime)-10s %(lineno) -5d: %(message)s"

    def __init__(
            self,
            username: str,
            password: str,
            host: str,
            port: int = 15672,
            heartbeat: int = 5,
            prefetch: int = 3,
            log_level: Optional[int] = logging.INFO,
            log_format: Optional[str] = None,
    ):
        """
        :param username: 队列用户名
        :param password: 队列密码
        :param host: 队列主机地址
        :param port: 队列主机端口
        :param heartbeat: 心跳
        :param prefetch: 队列流量数
        :param log_level: 日志等级
        :param log_format: 日志格式
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.heartbeat = heartbeat
        self.prefetch = prefetch
        # 队列名与处理函数的映射体
        self.queue_map = {}
        # 队列连接对象
        self.connection = None
        # 频道对象
        self.channel = None
        self.logger = self.create_logger(log_level, log_format)
        self.lock = Lock()  # 添加全局锁， 需要使用的时候创建

    def create_logger(self, log_level, log_format):
        """
        创建日志对象
        :param log_level: 日志等级
        :param log_format: 日志格式
        :return:
        """
        log_format = self.DEFAULT_LOG_FORMAT if not log_format else log_format
        logger = logging.getLogger(__name__)
        logging.basicConfig(level=log_level, format=log_format)
        return logger

    def add_to_queue_map(self, queue_name: str, func: Callable, auto_ack: bool, prefetch: int, service, **config_map):
        """
        添加队列名与执行函数的映射到 queue_map 中去
        :param queue_name: 队列名
        :param func: 执行函数
        :param auto_ack: 是否自动回复队列
        :param prefetch: 队列流量数
        :return:
        """
        queue = Queue(queue_name, func, auto_ack=auto_ack, prefetch=prefetch, service=service, **config_map)
        self.queue_map[queue_name] = queue

    def register(
            self,
            queue_name: str,
            auto_ack: bool = False,
            prefetch: int = 3,
            service=None,
            **config_map,
    ):
        """
        注册队列名及其执行函数
        :param queue_name: 队列名
        :param auto_ack: 是否自动回复队列
        :param prefetch: 流量数
        :param service: 流量数
        :return:
        """

        def _register(func: Callable):
            """
            :param func: 执行函数
            :return:
            """
            self.add_to_queue_map(queue_name, func, auto_ack, prefetch, service, **config_map)
            return func

        return _register

    def get_context(
            self,
            queue: Queue,
            channel,
            method_frame,
            header_frame,
            body: bytes,
            service

    ) -> Context:
        """
        将获取的消息进行封装，等到context对象
        :return: context实例
        """
        context = Context(queue, self.logger, self.connection, channel,
                          method_frame, header_frame, body, service, lock=self.lock)

        return context
