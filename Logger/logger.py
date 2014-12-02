# -*- encoding: utf-8 -*-

import sys
import logging

from .models import ModelLogger
from Desire.BaseFrameWork.Logger import models
from Desire.BaseFrameWork.Database import db_session


LOG_LEVEL = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARN': logging.WARN,
    'CRIT': logging.CRITICAL,
    'ERROR': logging.ERROR
}


class _Logger(object):
    def __init__(self, app_name, log_file=None, level="DEBUG", use_db=False):
        if use_db:
            models.init()
        self.app_name = app_name
        self.use_db = use_db
        if self.use_db:
            self.session = db_session.get_session()
        self.level = LOG_LEVEL[level] if level in LOG_LEVEL else logging.DEBUG
        self.logger = logging.getLogger(app_name)

        if log_file is None:
            self.log_handler = logging.StreamHandler(sys.stdout)
        else:
            self.log_handler = logging.FileHandler(log_file)
        self.logger.setLevel(self.level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(formatter)

        self.logger.addHandler(self.log_handler)

    def log(self, mod_name, level, message):
        dst_level = LOG_LEVEL[level] if level in LOG_LEVEL else logging.DEBUG

        if self.use_db and dst_level >= self.level:
            session = self.session

            new_record = ModelLogger()
            new_record.app_name = self.app_name
            new_record.level = dst_level
            new_record.mod_name = mod_name
            new_record.message = message

            session.add(new_record)
            session.commit()

        dst_message = "(%s) - %s" % (mod_name, message)
        self.logger.log(dst_level, dst_message)


_LOGGER = None


def init_logger(app_name, log_file=None, level="DEBUG", use_db=False):
    global _LOGGER

    _LOGGER = _Logger(app_name, log_file, level, use_db)


def get_logger():
    global _LOGGER

    return _LOGGER