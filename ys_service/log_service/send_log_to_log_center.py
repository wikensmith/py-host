#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2020/3/18 11:06
# @Author  : wiken
# @Site    : 
# @File    : send_log_to_log_center.py
# @Software: PyCharm
# @Desc    :
import json
import time

import requests
# from ys_service.queue_service.context import Context
SAVE_TO_LOG_CENTER_URL = "http://192.168.0.212:8081/log/save"
# from ys_service import SAVE_TO_LOG_CENTER_URL
from datetime import datetime, timezone, timedelta


def get_time():
    """
    获取当前东8区的时间字符串
    :return:
    """
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    now_zone8 = now.astimezone(timezone(timedelta(hours=8)))

    return now_zone8.isoformat()


def send_to_log_center(context, project, module, user, return_msg, level, **kwargs):
    """
    send msg to log_center
    :param context:
    :param project:
    :param module:
    :param user:
    :param return_msg:
    :param level:
    :param kwargs: field1, field2, field3, field4, field5
    :return:
    """

    # 数据组成
    msg_data = {
        "队列名称": context.queue.queue_name,
        "传入数据:": context.text,
        "返回数据": return_msg
    }
    # 请求数据
    request_data = {
        "project": project,
        "module": module,
        "level": level,
        "user": user,
        "message": json.dumps(msg_data, ensure_ascii=False),
        "time": get_time()
    }
    request_data.update(kwargs)

    r = requests.post(SAVE_TO_LOG_CENTER_URL, json=request_data)
    return r.text
