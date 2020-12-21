
# encoding=utf8
import functools
import json
import threading
import time
from json import JSONDecodeError
from typing import Callable

import pika
from pika.exceptions import ConnectionWrongStateError, ConnectionClosedByBroker

# from SC_B2B.sc_refund import do_refund


class MsgTopicCustomer(object):
    def __init__(self, username: str, password: str, queue: str, host: str, port: int = 5672, virtual_host: str = "/",
                 heartbeat: int = 5, prefetch_count: int = 1):
        """
        MsgRpcServer初始化
        :param username: RabbitMQ主机的用户名
        :param password: RabbitMQ主机的密码
        :param queue: 服务端监听的队列
        :param host: RabbitMQ主机的IP地址
        :param port: RabbitMQ主机的端口
        :param virtual_host: 服务端绑定的虚拟主机名
        :param heartbeat: 连接后，客户端与RabbitMQ主机保持心跳检测的超时时间
        :param prefetch_count: 从队列中预取消息的数量
        """
        credentials = pika.PlainCredentials(username, password)  # 创建配置对象
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host, port, virtual_host, credentials, heartbeat=heartbeat))  # 连接MQ主机
        self.channel = self.connection.channel()  # 创建通道
        self.channel.basic_qos(prefetch_count=prefetch_count)  # 配置消息预取数量(不意味着并发处理数量)
        self.channel.basic_consume(queue=queue, on_message_callback=self.on_request)  # 配置监听的消息队列和回调函数

        print(f"已运行,监听的队列: {queue} ")
        self.channel.start_consuming()  # 开始监听队列

    def multi_threading_do_data(self, ch, method, props, data, header_frame):
        """
        多线程数据处理
        """
        thread = threading.Thread(target=self.do_data, args=(ch, method, props, data, header_frame))
        thread.start()


    def on_request(self, ch, method, props, body):
        """
        消息处理函数(被basic_consume方法回调)
        :param ch: basic_consume方法回调的参数→channel
        :param method: basic_consume方法回调的参数→method
        :param props:basic_consume方法回调的参数→properties
        :param body:basic_consume方法回调的参数→body(二进制的消息内容)
        :return:None
        """
        header = props.headers()
        print(header)

        data = body.decode()
        self.multi_threading_do_data(ch, method, props, data, header_frame)

    def do_data(self, ch, method, props, data: str):
        print(f"接收到数据:{data}")
        # ---------↓虚线内为数据处理模拟过程(可替换),生成result_info_dict值↓--------------------
        try:
            param_info = json.loads(data)
            # result_info_dict = do_refund(p_=param_info)
            # print(result_info_dict)
        except JSONDecodeError:
            print("json数据格式错误")
            result_info_dict = {"status": 1, "msg": "json数据格式错误"}
        except Exception as e:
            print(f"异常→{e}")
            result_info_dict = {"status": 1, "msg": f"异常→{e}"}
        # ----------↑虚线内为数据处理模拟过程(可替换),生成result_info_dict值↑-------------------
        # if props.reply_to:
        back_message = functools.partial(self.back_message, *(
            ch, 'YS.机票.退票', 'ys.buychannel.refund.update', result_info_dict,
            pika.BasicProperties(correlation_id=props.correlation_id)))
        self.connection.add_callback_threadsafe(callback=back_message)  # connection对象负责调度自身线程下的事务处理，已避开冲突
        ack_message = functools.partial(self.ack_message, ch, method.delivery_tag, True)
        self.connection.add_callback_threadsafe(callback=ack_message)  # # connection对象负责调度自身线程下的事务处理，已避开冲突

    @staticmethod
    def back_message(ch, back_exchange, back_routing_key: str, data_dict: dict, properties):
        """
        回传消息
        """
        result_info_json = json.dumps(data_dict, ensure_ascii=False)
        ch.basic_publish(exchange=back_exchange, routing_key=back_routing_key, properties=properties,
                         body=result_info_json)
        print(f"返回数据:{result_info_json}")

    @staticmethod
    def ack_message(ch, delivery_tag, is_ack):
        """
        ACK队列
        """
        if ch.is_open:
            if is_ack:
                ch.basic_ack(delivery_tag)
            else:
                ch.basic_nack(delivery_tag)
        else:
            pass


if __name__ == '__main__':
    param = (
        ("username", "ys"),
        ("password", "ysmq"),
        ("queue", "YS.机票.国内.退票.wiken.DEBUG"),
        ("host", "192.168.0.100"),
        ("port", 5672),
        ("virtual_host", "/"),
        ("heartbeat", 5),
        ("prefetch_count", 1)
    )
    while True:
        try:
            MsgTopicCustomer(**dict(param))
        except ConnectionWrongStateError:
            print("MQ主机连接状态异常")
            time.sleep(1)
        except ConnectionClosedByBroker:
            time.sleep(1)
            print("MQ主机连接被强行断开")
        except Exception as f:
            time.sleep(1)
            print(f"其他异常:→{f}")
