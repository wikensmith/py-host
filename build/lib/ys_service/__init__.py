#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/7 9:53
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : __init__.py.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :
from ys_service.queue_service import BlockService
from ys_service.queue_service.context import Context
from ys_service.host import Host

# 保存日志至日志中心地址


ys_host = Host("ys", "ysmq", "192.168.0.100", thread_num=10, log_level=None)


__all__ = ["ys_host", "Context"]
