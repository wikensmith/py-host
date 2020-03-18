#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2020/3/18 11:06
# @Author  : wiken
# @Site    : 
# @File    : send_log_to_log_center.py
# @Software: PyCharm
# @Desc    :
import json

import requests
from ..queue_service.context import Context
from .. import SAVE_TO_LOG_CENTER_URL


def send_to_log_center(context: Context, project, module, user, return_msg, level, *args):
    """
    send msg to log_center
    :param context:
    :param project:
    :param module:
    :param user:
    :param return_msg:
    :param level:
    :param args: field1, field2, field3, field4, field5
    :return:
    """

    # 数据组成
    msg_data = {
        "queue_name": context.queue.queue_name,
        "input_parameters": context.text,
        "return_msg": return_msg
    }
    # 请求数据
    request_data = {
        "project": project,
        "module": module,
        "level": level,
        "user": user,
        "message": json.dumps(msg_data, ensure_ascii=False),
    }

    for k, arg in enumerate(args):
        request_data["field" + str(k+1)] = arg

    r = requests.post(SAVE_TO_LOG_CENTER_URL, json=request_data)
    return r.text
