# -*- encoding: utf-8 -*-

import sys
import logging

from .models import ModelLogger
from Desire.FrameWork.Logger import models
from Desire.FrameWork.Database import db_session


def read(*args, **kwargs):
    """
        从数据中读取Log
    """
    if "page" in kwargs:
        pass

    if "limit" in kwargs:
        pass

    if "order" in kwargs:
        pass

    pass