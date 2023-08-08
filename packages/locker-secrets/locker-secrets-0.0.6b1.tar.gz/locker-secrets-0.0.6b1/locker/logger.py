import logging
import os
import socket
import traceback

import locker


LOCKER_LOG = os.environ.get("LOCKER_LOG")


class Logger:
    def __init__(self):
        format_string = '%(asctime)s {hostname} %(levelname)s %(message)s'.format(**{'hostname': self._get_hostname()})
        format_log = logging.Formatter(format_string)

        logging.basicConfig(level=self._level_log())
        self.locker_logger = logging.getLogger("locker")
        for handler in self.locker_logger.handlers:
            self.locker_logger.removeHandler(handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(format_log)
        self.locker_logger.addHandler(stream_handler)

    @staticmethod
    def _get_hostname():
        return socket.gethostname()

    @staticmethod
    def _level_log():
        _map_level_log = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR
        }
        if locker.log in _map_level_log.keys():
            return _map_level_log[locker.log]
        elif LOCKER_LOG in _map_level_log.keys():
            return _map_level_log[LOCKER_LOG]
        else:
            return logging.NOTSET

    def debug(self, msg):
        self.locker_logger.setLevel(self._level_log())
        self.locker_logger.debug(msg)

    def info(self, msg):
        self.locker_logger.setLevel(self._level_log())
        self.locker_logger.info(msg)

    def warning(self, msg):
        self.locker_logger.setLevel(self._level_log())
        self.locker_logger.warning(msg)

    def error(self, trace=None):
        self.locker_logger.setLevel(self._level_log())
        if trace is None:
            tb = traceback.format_exc()
            trace = 'Something was wrong' if tb is None else tb
        self.locker_logger.error(trace)


logger = Logger()
