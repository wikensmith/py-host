#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/4 17:37
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : setup.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    detail_description = f.read()

requirement = [
    "APScheduler==3.6.3",
    "certifi==2019.9.11",
    "chardet==3.0.4",
    "idna==2.8",
    "pika==1.1.0",
    "pymongo==3.9.0",
    "pymssql==2.1.4",
    "PyMySQL==0.9.3",
    "python-dateutil==2.8.1",
    "python-redis-lock==3.3.1",
    "pytz==2019.3",
    "redis==3.3.11",
    "redlock-py==1.0.8",
    "requests==2.22.0",
    "retrying==1.3.3",
    "six==1.13.0",
    "suds-py3==1.3.4.0",
    "tzlocal==2.0.0",
    "urllib3==1.25.7",
]


setuptools.setup(
    name="py_host",
    version="0.0.8",
    author="wiken",
    author_email="wiken01@qq.com",
    description="modify format of msg to log center of ys.",
    url="https://github.com/wikensmith/py-host.git",
    long_description=detail_description,
    long_description_content_type="text/markdown",
    install_requires=requirement,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
