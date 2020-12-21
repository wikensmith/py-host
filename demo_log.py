#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/29 11:37
# @Author  : wiken
# @Site    : 
# @File    : demo_log.py
# @Software: PyCharm
# @Desc    :
from ys_service import *


@ys_host.register("YS.机票.国内.退票.wiken.DEBUG", prefetch=1, consumer_tag="wikenlala")
def refund(context):
    print("bigin:", context.text)
    re = context.send_log_to_center(
        context=context,
        project="wikenTest",
        module="test1",
        user="7921",
        level="error",
        return_msg="log_center_test",
        field1="111111",
        field2="自愿",
        field3="国内",
    )

    print("result:", re)
    # context.ack()
    context.nack()


with ys_host:
    ys_host.start()
