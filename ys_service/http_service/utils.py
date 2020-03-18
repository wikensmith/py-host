#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/14 16:10
# @Author  : wiken
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
# @Desc    :
import hashlib
from json.decoder import JSONDecodeError


def check_http_response(res):
    """
    检查返回的http response 是否是需要的数据
    :param res:
    :return: dict
    """
    if isinstance(res, dict):
        return res
    try:
        dic = res.json()
    except (AttributeError, JSONDecodeError) as e:
        print(e)
        return None

    else:
        return dic


def return_msg(is_success, status_code=None, msg=None, data=None):
    return {
        "is_success": is_success,
        "status_code": status_code,
        "message": msg,
        "data": data
    }


def convert_time(_date):
    # '11/19/19 11:48:50 AM'
    import datetime
    if _date.count("/") == 2 and _date.count(":") == 2:
        date = _date[:-3]
        date = datetime.datetime.strptime(date, "%m/%d/%y %H:%M:%S")
        if "PM" in _date:
            date += datetime.timedelta(hours=12)
        return date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return _date


def convert_to_lower(dic):
    """
    把字典中地健值全部转换为小写字母
    :param dic:
    :return:
    """
    lower_dic = {}
    for k, v in dic.items():
        if isinstance(v, list):
            temp_v = []
            for i in v:
                temp_d = {}
                for k2, v2 in i.items():
                    # print(v2)
                    temp_d[k2.lower()] = v2
                temp_v.append(temp_d)
            f_v = temp_v
        elif isinstance(v, dict):
            temp_v = {}
            for k2, v2 in v.items():
                temp_v[k2.lower()] = v2
            f_v = temp_v
        else:
            f_v = v
        lower_dic[k.lower()] = f_v
    return lower_dic


def md5_encrypt(info):
    """
    md5 加密
    :param info:
    :return:
    """
    # s = "15922908607"
    a = hashlib.md5()
    a.update(info.encode(encoding='utf-8'))
    return a.hexdigest()
# print(convert_time('11/19/19 11:48:50 PM'), type(convert_time('11/19/19 11:48:50 PM')))


__all__ = ["md5_encrypt", "convert_to_lower", "convert_time", "check_http_response", "return_msg"]
