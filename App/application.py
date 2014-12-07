# -*- encoding:utf-8 -*-
__author__ = "shuhao.wang"

import sys
import os
import copy

from Desire.BaseFramework.Database import db_engine
from Desire.BaseFramework.Logger import logger


class Application(object):
    def __init__(self, *args, **kwargs):
        self.app_name = kwargs['app_name'] if "app_name" in kwargs else "Desire"
        self.args = copy.deepcopy(args)
        self.kwargs = copy.deepcopy(kwargs)
        if 'app_name' in self.kwargs:
            del self.kwargs['app_name']

        self.app_entry = None
        self._init()

    def _init(self):
        sys.path.append(os.getcwd())

        setting = __import__("setting.settings")
        settings = setting.settings

        debug = False
        if hasattr(settings, "DEBUG"):
            debug = settings.DEBUG

        if hasattr(settings, "APP_CLASS"):
            self.app_entry = settings.APP_CLASS

        # initialize database
        has_db = False
        if hasattr(settings, "DATABASE"):
            db_engine.init_engine(settings.DATABASE, debug)
            has_db = True

        # initialize logger
        logger_file = None
        if hasattr(settings, "LOGGER_FILE"):
            logger_file = settings.LOGGER_FILE

        logger_level = "DEBUG"
        if hasattr(settings, "LOGGER_LEVEL"):
            logger_level = settings.LOGGER_LEVEL

        if debug:
            logger_level = "DEBUG"

        use_db = False
        if hasattr(settings, "LOGGER_DB"):
            use_db = settings.LOGGER_DB and has_db

        logger.init_logger(self.app_name, logger_file, logger_level, use_db=use_db)

    def start(self):
        if self.app_entry:
            self.app_entry(*self.args, **self.kwargs)
        else:
            raise SystemError("No application entry")
