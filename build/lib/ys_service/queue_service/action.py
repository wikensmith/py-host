#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/5 15:57
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : action.py
# @project : ys_module
# @Software: PyCharm
# @Desc    : 回复的动作
import uuid
import pika
import json
from functools import partial
from typing import Union


class Action(object):

    def __init__(self, context):
        self.context = context
        self.queue = context.queue
        self.body = context.body
        self.method_frame = context.method_frame
        self.header_frame = context.header_frame
        self.chan = context.chan
        self.conn = context.conn

    def _publish(
            self,
            exchange_name=None,
            routing_key=None,
            new_message: Union[str, bytes]=None,
            properties=None,
    ):
        """
        生产消息
        :param exchange_name:
        :param routing_key:
        :param new_message: 新消息内容
        :param properties:
        :return:
        """
        body = self.get_body(new_message)
        self.conn.add_callback_threadsafe(
            partial(self.chan.basic_publish, exchange_name, routing_key, body, properties=properties)
        )

    @staticmethod
    def get_body(data):
        """
        返回数据的二进制格式
        :param data:
        :return:
        """

        if isinstance(data, bytes):
            return data
        try:
            return json.dumps(data, ensure_ascii=False).encode("utf-8")
        except json.JSONDecodeError:
            return data.encode("utf-8")

    @property
    def delivery_tag(self):
        return self.context.delivery_tag


class ActionAck(Action):

    exchange = "system.response"

    def __init__(self, context, reply_data=""):
        super().__init__(context)
        self.reply_data = reply_data

    def __call__(self, *args, **kwargs):
        reply_to = self.header_frame.reply_to

        # 当有replay_to的时候，向replay_to发送信息
        if reply_to:
            properties = pika.BasicProperties(
                correlation_id=self.header_frame.correlation_id,
                message_id=str(uuid.uuid1())
            )
            self._publish(self.exchange, reply_to, self.reply_data, properties=properties)

        self.conn.add_callback_threadsafe(partial(self.chan.basic_ack, self.delivery_tag))


class ActionNack(Action):

    def __call__(self, *args, **kwargs):
        self.conn.add_callback_threadsafe(partial(self.chan.basic_nack, self.delivery_tag))


class ActionNextTo(Action):

    def __init__(self, context, exchange_name, routing_key, new_message_data, new_message_headers):
        Action.__init__(self, context)
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.new_message_data = new_message_data
        self.new_message_headers = new_message_headers

    def __call__(self, *args, **kwargs):
        # 当没有新的消息header时，copy原来的headers
        headers = self.get_headers()
        data = self.get_body(self.new_message_data) if self.new_message_data else self.context.body
        properties = pika.BasicProperties(
            headers=headers,
        )
        self._publish(self.exchange_name, self.routing_key, data, properties)
        self.conn.add_callback_threadsafe(partial(self.chan.basic_ack, self.delivery_tag))

    def get_headers(self):
        """
        获取头部信息, 并且设定processID
        :return:
        """
        old_header = getattr(self.context.header_frame, "headers", {})
        if not self.new_message_headers:
            headers = old_header
        else:
            headers = self.new_message_headers
            for i, v in old_header.items():
                # 当新头部中有与context的header中相同的字段的时候，不作改变
                if headers.get(i):
                    continue
                # 当新头中没有i键的时候，设置新头的i键的值为v
                headers[i] = v
        headers["processID"] = str(uuid.uuid1())
        headers["traceID"] = old_header.get("traceID")
        return headers


class ActionGoBack(Action):

    def __init__(self, context, timing=None):
        """
        :param context:
        :param timing: 延迟执行或者定时执行时间表达式
        """
        super().__init__(context)
        self.timing = timing

    def __call__(self, *args, **kwargs):
        self._publish()
