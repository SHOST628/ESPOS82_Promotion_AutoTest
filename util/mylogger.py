from logging import handlers
from frozen_path import cur_path
from util.readconfig import log_file
from util.mk_folder import mkdir
from util.readconfig import debug_level
import logging
import os
import sys


class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'critical':logging.CRITICAL
    }

    def __init__(self, filename, filelevel='debug', streamlevel='info', when='D',interval=1, backupCount=10, fformatter='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s', sformatter='%(asctime)s - %(message)s'):
        project_path = cur_path()
        self.folder = os.path.join(project_path, 'logs')
        mkdir(self.folder)
        self.filename = os.path.join(self.folder, filename)
        # set logger format
        self.file_formatter = logging.Formatter(fformatter)
        self.stream_formatter = logging.Formatter(sformatter)
        self.filelevel = filelevel
        self.streamlevel = streamlevel
        self.when = when
        self.interval = interval
        self.backupcount = backupCount
        self.logger = logging.getLogger(self.filename)
        self.logger.setLevel(self.level_relations.get(self.filelevel))  # set logger level

    def _output(self,level,message):
        # stop output to console
        sh = logging.StreamHandler()
        sh.setLevel(self.level_relations.get(self.streamlevel))
        sh.setFormatter(self.stream_formatter)
        # th = handlers.TimedRotatingFileHandler(filename=self.filename, when=self.when, interval=self.interval, backupCount=self.backupcount, encoding='utf-8')  # separate file by time
        # th.setFormatter(self.file_formatter)
        self.logger.addHandler(sh)
        # self.logger.addHandler(th)
        if level == 'debug':
            self.logger.debug(message)
        elif level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # elif level == 'exception':
        #     self.logger.exception(message)
        elif level == 'critical':
            self.logger.critical(message)
        # self.logger.removeHandler(th)
        self.logger.removeHandler(sh)
        # th.close()

    def debug(self,message):
        self._output('debug',message)

    def info(self,message):
        self._output('info',message)

    def warning(self,message):
        self._output('warning',message)

    def error(self,message):
        self._output('error',message)

    def exception(self,message):
        self._output('exception',message)

    def critical(self,message):
        self._output('critical',message)


class MyLogger(logging.Logger):
    def __init__(self, logger_name='mylog', file_name=None, log_file=1, level='debug', when='D', interval=1, backupCount=10, encoding='utf-8',
                 fformatter='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s',
                 sformatter='%(asctime)s - %(message)s'):
        super().__init__(logger_name)
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False
        stream_formatter = logging.Formatter(sformatter)  # set logger format
        self.logger.setLevel(level)  # set logger level
        # sh = logging.StreamHandler()
        # sh.setLevel(level)
        # sh.setFormatter(stream_formatter)
        # self.logger.addHandler(sh)
        if log_file:
            project_path = cur_path()
            folder = os.path.join(project_path, 'logs')
            file_name = os.path.join(folder, file_name)
            mkdir(folder)
            self.th = handlers.TimedRotatingFileHandler(filename=file_name, when=when,
                                                   interval=interval, backupCount=backupCount, encoding=encoding)  # separate file by time
            file_formatter = logging.Formatter(fformatter)
            self.th.setLevel(level)
            self.th.setFormatter(file_formatter)
            self.logger.addHandler(self.th)

    def rlogger(self):
        return self.logger


if log_file == '':
    log_file = 0
else:
    log_file = int(log_file)
if debug_level.upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR',  'CRITICAL']:
    logger = MyLogger(file_name='case.log', log_file=log_file, level=debug_level.upper()).rlogger()
else:
    logger = MyLogger(file_name='case.log', log_file=log_file, level='INFO').rlogger()



# if debug_level.lower() in ['debug', 'info', 'warning', 'error',  'critical']:
#     logger = Logger(filename='case.log', filelevel=debug_level.lower())
# else:
#     logger = Logger(filename='case.log', filelevel='info')