#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/4 14:00
# @Author  : 7913
# @Site    : https://github.com/v5yangzai
# @File    : server.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :
import logging
from pika.channel import Channel
from typing import Callable, Optional
from concurrent.futures import ThreadPoolExecutor

from ys_service.queue_service.context import Context
from ys_service.queue_service.queue import Queue
from ys_service.queue_service.action import *
from ys_service.queue_service.base_service import BaseService


class BlockService(BaseService):

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
        super().__init__(username, password, host, port, heartbeat, prefetch, log_level, log_format)
        self.thread_num = thread_num
        self._thread_executor = ThreadPoolExecutor(max_workers=thread_num)

    def connect_queue(self):
        """
        连接到队列上
        :return:
        """
        self.logger.info("正在与队列建立连接")
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            self.host,
            credentials=credentials,
            heartbeat=self.heartbeat
        )

        connection = pika.BlockingConnection(parameters=parameters)
        self.logger.info("队列连接成功")
        self.connection = connection

    def listen_queue(self):
        """
        监听到注册的队列
        :return:
        """
        # 创建channel
        channel = self.connection.channel()
        for _, queue in self.queue_map.items():
            print("queue name", queue.queue_name)
            channel.basic_qos(prefetch_count=queue.prefetch)
            channel.basic_consume(
                queue=queue.queue_name,
                on_message_callback=self.on_message(queue.func, queue),
                auto_ack=queue.auto_ack,
            )
            self.logger.info(f"队列<{queue.queue_name}>监听中...")
        self.logger.info("开始消费")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            self.logger.error("中断消费。。。")
            channel.stop_consuming()

    def on_message(self, func: Callable, queue: Queue):
        """
        用于并发处理消息
        :param func: 处理函数
        :param queue: 队列对象
        :return:
        """
        func = partial(self.handler_func, func, queue)
        return func

    def handler_func(
            self,
            func: Callable,
            queue: Queue,
            channel: Channel,
            method_frame,
            header_frame,
            body: bytes
    ):
        context = self.get_context(queue, channel, method_frame, header_frame, body, queue.service)
        self._thread_executor.submit(self.handler, func, context)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.error("队列关闭")
        self.connection.close()

    def start(self):
        self.connect_queue()
        self.listen_queue()

    @staticmethod
    def handler(func: Callable, context: Context):
        """
        jie
        :param func: 处理函数
        :param context: Context对象
        :return:
        """
        result = func(context)
        if callable(result):
            result()
