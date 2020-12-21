#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/11 17:19
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : service_provider.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :
import json
import time
from decimal import Decimal
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

from ys_service.log_service.local_log import info_log, error_log
from ys_service.db_service import DBService, MongoService, MysqlService, RedisService, SqlServerService
from ys_service.http_service.mq_service import CreateMQ
from ys_service.http_service.log_service import LogCreate
from ys_service.http_service.http_service import HTTPService
from ys_service.http_service.attach_data_service import CreateAttachDataService
from ys_service.http_service.reservation_service import CreateReservation
from ys_service.http_service.config_center_service import CreateConfigCenterService
from ys_service.http_service.realtime_notice_service import CreateRealtimeNoticeService
from ys_service.http_service.web_service_client import CreateWebServiceClient
from ys_service.http_service.ys_requests import YsRequests


class ServiceProvider(object):

    def __init__(self):
        # 数据库对象
        self.db_service = DBService()
        self.http_service = HTTPService()
        self._thread_pool = None
        self._logger = None

    @property
    def mongo_client(self) -> MongoService:
        """
        获取mongo服务
        :return:
        """
        return self.db_service.mongo_client

    @property
    def mysql_client(self) -> MysqlService:
        """
        获取mysql服务
        :return:
        """
        return self.db_service.mysql_client

    @property
    def redis_client(self) -> RedisService:
        """
        获取redis服务
        :return:
        """
        return self.db_service.redis_client

    @property
    def sql_server_client(self) -> SqlServerService:
        return self.db_service.sql_server_client

    def _strptime(self, time_str, f=None):
        """
        将时间字符串格式化为时间类型
        :param f: 时间格式
        :param time_str: 时间字符串
        :return:
        """
        if f:
            return datetime.strptime(time_str, f)

        try:
            return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, "%Y-%m-%d")
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, "%Y/%m/%d")
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S AM")
        except ValueError:
            pass

        try:
            d = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S PM")
            return d + self.timedelta(hours=12)
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f0")
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S.%f0")
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, "%m/%d/%Y %H:%M:%S")
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, f"%m-%d-%y %H:%M:%S AM")
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, f"%m/%d/%y %H:%M:%S AM")
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, f"%m-%d-%y %H:%M:%S PM") + self.timedelta(hours=12)
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, f"%m/%d/%y %H:%M:%S PM") + self.timedelta(hours=12)
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, f"%Y-%m-%d %H:%M")
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, f"%Y/%m/%d %H:%M")
        except ValueError:
            pass

        try:
            return datetime.strptime(time_str, f"%Y/%m/%d %H:%M:%S")
        except ValueError:
            pass

    def strptime(self, time_str, f=None):
        return self._strptime(time_str, f) - self.timedelta(hours=8)

    @property
    def time(self):
        """
        获取
        :return:
        """
        return time

    @property
    def datetime(self):
        return datetime

    @property
    def timedelta(self):
        return timedelta

    @staticmethod
    def marshal(value):
        return json.dumps(value, ensure_ascii=False)

    @property
    def now(self):
        return datetime.utcnow()

    @property
    def local_now(self):
        return datetime.now()

    def get_three_code(self, s):
        redis = self.redis_client.connect(host="192.168.0.100", port=6379, password="O0qtw1wHPddwCC5T", db=0)
        d = redis.hget("System:BaseInfo:AirlineInfo", s)

        return json.loads(d).get("ThreeCode") if d else ""

    @staticmethod
    def parse_to_float(d):

        try:
            money = float(d)
        except ValueError:
            money = 0
        return money

    @staticmethod
    def parse_to_decimal(d):

        try:
            money = Decimal(d)
        except ValueError:
            money = Decimal(0)
        return money

    @ property
    def log_factory(self):
        """
        创建日志中心对象
        :return:
        """
        return LogCreate()

    @property
    def mq_service(self):
        """
        创建mq服务对象
        :return:
        """
        print("CreateWebServiceClient", CreateWebServiceClient)
        return CreateMQ()

    @property
    def reservation_service(self):
        """
        创建预约服务对象
        :return:
        """
        return CreateReservation()

    @property
    def realtime_notice_service(self):
        """
        创建定时消息对象
        :return:
        """
        return CreateRealtimeNoticeService()

    @property
    def config_center_service(self):
        """
        创建配置中心对象
        :return:
        """
        return CreateConfigCenterService()

    @property
    def attach_data_service(self):
        """
        获取附加消息对象
        :return:
        """
        return CreateAttachDataService()

    @property
    def ws_client(self):
        """
        获取webservice client对象
        :return:
        """
        return CreateWebServiceClient()

    @property
    def ys_requests(self):
        return YsRequests

    def log(self, message, level="info", data_property=None, version=None, auth=None,
            application_name=None, application_module=None, process_stage=None, header=None):

        if not self._logger:
            application = {
                "applicationName": application_name,
                "applicationVersion": version,
                "applicationModule": application_module,
                "author": auth
            }
            header = header
            trace_property = {
                "traceId": header.get("trace_id"),
                "processId": header.get("process_id"),
                "processStage": process_stage or header.get("process_stage")
            }
            self._logger = LogCreate().create(application, trace_property)
        if not data_property:
            data_property = {
                "StatusCode": 200 if level == "info" else 400,
                "StatusDesc": "执行成功" if level == "info" else "执行失败"
            }

        self._logger.send_log(message, level=level, data_property=data_property)

    def local_log(self, msg, level="info", is_net=False, application_name=None, process_stage=None,
                  **kwargs):
        """
        将日志打印到本地, 当is_net为True时， application_name 为必填
        :param msg: 日志内容
        :param level: 日志等级 支持info、 error
        :param is_net: 是否上传到网络日志（kibana）
        :param process_stage: kibana中根据该字段分类。
        :param application_name: kibana 中可根据该字段查询
        :return: None
        """
        msg = msg
        if not self._thread_pool:
            self._thread_pool = ThreadPoolExecutor(10)

        if level == "info":
            self._thread_pool.submit(info_log.logger.info, msg)
        else:
            self._thread_pool.submit(error_log.logger.error, msg)

        if is_net:
            arg_1 = "success" if level == "info" else msg[:200]
            self.log(arg_1,
                     level,
                     application_name=application_name,
                     process_stage=process_stage,
                     **kwargs
                     )
