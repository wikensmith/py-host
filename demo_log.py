#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/29 11:37
# @Author  : wiken
# @Site    : 
# @File    : demo_log.py
# @Software: PyCharm
# @Desc    :
import json
import traceback
from datetime import datetime
from ys_service import *


@ys_host.register("YS.机票.国内.退票.wiken.DEBUG", prefetch=1)
def refund(context):

    re = context.send_log_to_center(
        context=context,
        project="51bookRefund",
        module="domestic",
        user="7921",
        level="info",
        return_msg="result_msg",
        field1="ss",
        field2="自愿",
        field3="国内",
    )
    print("result:", re)
    pass

with ys_host:
    ys_host.start()