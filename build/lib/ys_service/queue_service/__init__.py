#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/4 13:59
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : __init__.py.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :
import logging
from typing import Optional
from ys_service.queue_service.block_service import BlockService


def get_block_server(
            username: str,
            password: str,
            host: str,
            port: int = 15672,
            heartbeat: int = 5,
            prefetch: int = 3,
            thread_num: Optional[int] = None,
            log_level: Optional[str] = logging.INFO,
            log_format: Optional[str] = None,
):

    return BlockService(
        username, password, host, port,
        heartbeat, prefetch, thread_num, log_level, log_format
    )


DEFAULT_SERVER = get_block_server("ys", "ysmq", "192.168.0.100", thread_num=10, log_level=None)
