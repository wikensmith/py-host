#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/4 14:35
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : context.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :
from bson.objectid import ObjectId
from ys_service.queue_service.action import *

from concurrent.futures import ThreadPoolExecutor
from ys_service.http_service.log_service import LogCreate
from ys_service.http_service.context_attach_data_server import ContextAttachDataServer
from ys_service.http_service.attach_data_service import CreateAttachDataService
from ys_service.log_service.local_log import info_log, error_log
from ys_service.log_service.send_log_to_log_center import send_to_log_center


class Context(object):
    """
    将获取的详细进行封装为Context对象
    """
    def __init__(self, queue, logger, connection, channel, method_frame, header_frame, body, service, lock):
        self.queue = queue
        self.logger = logger
        self.conn = connection
        self.chan = channel
        self.method_frame = method_frame
        self.header_frame = header_frame
        self.body = body
        self.timing = None  # 定时
        self.service = service
        self.object_id = ObjectId
        self.logger = None  # 日志对像
        self._context_attach_data_handler = None
        self._thread_pool = None
        self.lock = lock

    @property
    def delivery_tag(self):
        return self.method_frame.delivery_tag

    def ack(self, reply_data=None):
        return ActionAck(self, reply_data)()

    def nack(self):

        return ActionNack(self)()

    def next_to(
            self,
            exchange_name=None,
            routing_key=None,
            new_message_body=None,
            new_message_headers=None,
    ):
        return ActionNextTo(self, exchange_name, routing_key, new_message_body, new_message_headers)()

    def go_back(self, timing=None):
        return ActionGoBack(self, timing)()

    def get_header(self, key):
        return self.header_frame.headers.get(key)

    @property
    def text(self):
        """
        获取数据的字符串格式
        :return:
        """
        return self.body.decode("utf-8") if self.body else ""

    def get_json(self):
        """
        获取数据反序列化后的对象
        :return: 反序列化后的对象
        """
        try:
            return json.loads(self.text)
        except json.JSONDecodeError:
            return None

    @property
    def attach_data(self):

        if not self._context_attach_data_handler:
            attach_data_handler = CreateAttachDataService().create()
            try:
                message_id = self.get_json()["messageId"]
            except (TypeError, KeyError) as e:
                return {
                    "is_success": False,
                    "status_code": "",
                    "message": "从队列中获取message_id失败, 异常信息{}".format(e),
                    "data": self.body
                }
            self._context_attach_data_handler = ContextAttachDataServer(
                message_id=message_id,
                handler=attach_data_handler
            )

        return self._context_attach_data_handler

    def log(self, message, level="info", data_property=None, version=None, auth=None,
            application_name=None, application_module=None, process_stage=None):

        if not self.logger:
            application = {
                "applicationName": "py_host: " + (application_name or self.queue.queue_name),
                "applicationVersion": version,
                "applicationModule": application_module,
                "author": auth
            }
            header = {} if not self.header_frame.headers else self.header_frame.headers
            trace_property = {
                "traceId": header.get("trace_id"),
                "processId": header.get("process_id"),
                "processStage": process_stage or header.get("process_stage")
            }
            self.logger = LogCreate().create(application, trace_property)
        if not data_property:
            data_property = {
                "StatusCode": 200 if level == "info" else 400,
                "StatusDesc": "执行成功" if level == "info" else "执行失败"
            }

        self.logger.send_log(message, level=level, data_property=data_property)

    def local_log(self, msg, level="info", is_net=False, application_name=None, process_stage=None, **kwargs):
        """
        将日志打印到本地, 当is_net为True时， application_name 为必填
        :param msg: 日志内容
        :param level: 日志等级 支持info、 error
        :param is_net: 是否上传到网络日志（kibana）
        :param process_stage: kibana中根据该字段分类。
        :param application_name: kibana 中可根据该字段查询
        :return: None
        """
        log_info = "队列名称：{}\n传入数据:{}\n返回数据:{}\n".format(self.queue.queue_name, self.get_json(), msg)
        if not self._thread_pool:
            self._thread_pool = ThreadPoolExecutor(10)
        with self.lock:
            if level == "info":
                self._thread_pool.submit(info_log.logger.info, log_info)
            else:
                self._thread_pool.submit(error_log.logger.error, log_info)

        if is_net:
            arg_1 = "success" if level == "info" else msg[:200]
            # self._thread_pool.submit(self.log, arg_1, level=level,
            #                          application_name=application_name, process_stage=process_stage, **kwargs)
            #
            self.log(arg_1, level, application_name=application_name,
                     process_stage=process_stage, **kwargs)

    @property
    def send_log_to_center(self):
        return send_to_log_center
