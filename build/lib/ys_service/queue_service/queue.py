#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/4 14:45
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : queue.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :

from typing import Callable


class Queue(object):
    """
    监听的队列的实例
    """
    def __init__(
            self,
            queue_name: str,
            func: Callable,
            auto_ack: bool,
            prefetch: int,
            service,
            **config_map,
    ):
        """
        :param queue_name: 队列名
        :param func: 处理函数
        :param auto_ack: 是否自动回复队列
        :param prefetch: 队列流量数
        :param service: 服务
        """
        self.queue_name = queue_name
        self.func = func
        self.auto_ack = auto_ack
        self.prefetch = prefetch
        self.service = service
        self.consumer_tag = config_map.get("consumer_tag", None)
