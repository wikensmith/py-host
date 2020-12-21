import os
import time
import codecs
import logging

from logging import FileHandler
from pathlib import Path


class SafeFileHandler(FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=0):
        """
        Use the specified filename for streamed logging
        """
        if codecs is None:
            encoding = None
        FileHandler.__init__(self, filename, mode, encoding, delay)
        self.mode = mode
        self.encoding = encoding
        self.suffix = "%Y-%m-%d"
        self.suffix_time = ""

    def emit(self, record):
        """
        Emit a record.

        Always check time
        """
        try:
            if self.check_baseFilename(record):
                self.build_baseFilename()
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    # def check_baseFilename(self, record):
    #     """
    #     Determine if builder should occur.
    #
    #     record is not used, as we are just comparing times,
    #     but it is needed so the method signatures are the same
    #     """
    #     timeTuple = time.localtime()
    #
    #     if self.suffix_time != time.strftime(self.suffix, timeTuple) or not os.path.exists(
    #             self.baseFilename + '.' + self.suffix_time):
    #         return 1
    #     else:
    #         return 0

    def build_baseFilename(self):
        """
        do builder; in this case,
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # remove old suffix
        if self.suffix_time != "":
            index = self.baseFilename.find("." + self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # add new suffix
        currentTimeTuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, currentTimeTuple)
        self.baseFilename = self.baseFilename + "." + self.suffix_time

        self.mode = 'a'
        if not self.delay:
            self.stream = self._open()


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level,
                 fmt='%(asctime)s - %(levelname)s: \n%(message)s\n'):

        path = "{}".format(os.sep).join(os.getcwd().split("{}".format(os.sep)))
        path = "E:{a}logs{a}".format(a=os.sep) + path.split(os.sep)[-2]
        self.log_file_exist(path)
        self.filename = os.path.join(path, filename)
        if level == 'info':
            self.logger = logging.getLogger(self.filename)
            format_str = logging.Formatter(fmt)  # 设置日志格式
            self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
            # sh = logging.StreamHandler()  # 往屏幕上输出
            # sh.setFormatter(format_str)  # 设置屏幕上显示的格式
            th = SafeFileHandler(filename=self.filename, encoding='utf-8')
            # th.suffix = "%Y-%m-%d.log"
            th.setFormatter(format_str)  # 设置文件里写入的格式
            # self.logger.addHandler(sh)  # 把对象加到logger里
            self.logger.addHandler(th)
        else:
            self.logger = logging.getLogger(self.filename)
            format_str = logging.Formatter(fmt)  # 设置日志格式
            self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
            # sh = logging.StreamHandler()  # 往屏幕上输出
            # sh.setFormatter(format_str)  # 设置屏幕上显示的格式
            th = SafeFileHandler(filename=self.filename, encoding='utf-8')
            # th.suffix = "%Y-%m-%d.log"
            th.setFormatter(format_str)  # 设置文件里写入的格式
            self.logger.addHandler(th)  # 把对象加到logger里

    @staticmethod
    def log_file_exist(path):
        if not os.path.exists(path):
            p = Path(path)
            p.mkdir(parents=True)


info_log = Logger('info.log', level='info')
error_log = Logger('error.log', level='error')


if __name__ == '__main__':
    for i in range(10):
        # time.sleep(0.1)
        # time.sleep(1)
        print(i)
        info_log.logger.info("test: "+str(i))
        error_log.logger.error(i)
