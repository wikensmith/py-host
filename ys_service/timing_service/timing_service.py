#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/6 15:35
# @Author  : wiken
# @Site    : 
# @File    : timing_server.py
# @Software: PyCharm
# @Desc    :

from apscheduler.schedulers.background import BackgroundScheduler


class TimingService(object):

    cron = "cron"
    interval = "interval"
    date = "date"

    def __init__(self):

        self.func_list = []
        self.scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

    def timing_server(self, trigger, **kwargs):
        """
            使用示例：
            from queue_server.timing_server import TimingServer

            a = TimingServer()

            @a.timing_server(trigger="date", run_date="2019-11-06 23:13:40")
            def work():
                print("ssss")

            a.start()

            trigger q触发器取值分三种类型：
            1、 date
                在特定的时间点触发1次操作，示例如下：
                def job_func(text):
                    print(text)
                scheduler = BackgroundScheduler()
                # 在 2017-12-13 时刻运行一次 job_func 方法
                scheduler.add_job(job_func, 'date', run_date=date(2017, 12, 13), args=['text'])
                # 在 2017-12-13 14:00:00 时刻运行一次 job_func 方法
                scheduler.add_job(job_func, 'date', run_date=datetime(2017, 12, 13, 14, 0, 0), args=['text'])
                # 在 2017-12-13 14:00:01 时刻运行一次 job_func 方法
                scheduler .add_job(job_func, 'date', run_date='2017-12-13 14:00:01', args=['text'])
            2、 interval
                固定时间间隔触发， 参数如下：
                weeks (int) 	间隔几周
                days (int)  间隔几天
                hours (int)	 间隔几小时
                minutes (int)  间隔几分钟
                seconds (int)  间隔多少秒
                start_date (datetime 或 str)  开始日期
                end_date (datetime 或 str)  结束日期
                timezone (datetime.tzinfo 或str)  时区
                传参示例如下：
                # 每隔两分钟执行一次 job_func 方法
                scheduler .add_job(job_func, 'interval', minutes=2)
                # 在 2017-12-13 14:00:01 ~ 2017-12-13 14:00:10 之间, 每隔两分钟执行一次 job_func 方法
                scheduler .add_job(job_func, 'interval', minutes=2, start_date='2017-12-13 14:00:01' , end_date='2017-12-13 14:00:10')
            3、 cron
                参数如下：
                year (int 或 str)  年，4位数字
                month (int 或 str)  月 (范围1-12)
                day (int 或 str)  日 (范围1-31
                week (int 或 str)  周 (范围1-53)
                day_of_week (int 或 str)  周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun)
                hour (int 或 str)  时 (范围0-23)
                minute (int 或 str)	 分 (范围0-59)
                second (int 或 str) 	秒 (范围0-59)
                start_date (datetime 或 str)  最早开始日期(包含)
                end_date (datetime 或 str)  最晚结束时间(包含)
                timezone (datetime.tzinfo 或str)  指定时区
                除此还支持算数表达式， 如下：
                expression field    description
                *          any      fire on every value
                */a        any      fire every a values, starting from minimum
                a-b        any      fire on any value within the a-b range(a must be smaller than b)
                a-b/c      any      fire every c value within the a-b range
                xth y      day      fire on the x-th occurrence of weekday y within the month
                last x     day      fire on the last occurrence of weedkay x within the month
                last       day      fire on the last day within the month
                x,y,z      any      fire on any matching expresion; can combine any number of any of above expression
                示例如下：
                # 在每年 1-3、7-9 月份中的每个星期一、二中的 00:00, 01:00, 02:00 和 03:00 执行 job_func 任务
                scheduler .add_job(job_func, 'cron', month='1-3,7-9',day='0, tue', hour='0-3')

        :param str trigger: date, interval, cron
        :param dict kwargs:
        :return:
        """
        def timing(_func):
            job = Job(_func, trigger, times=kwargs)
            self.func_list.append(job)
            return _func

        return timing

    def start(self):
        for i in self.func_list:
            self.scheduler.add_job(i.func, trigger=i.trigger, **i.times)
        self.scheduler.start()


class Job(object):
    def __init__(self, _func, trigger=None, times=None):
        self.func = _func
        self.trigger = trigger
        self.times = times or {}
