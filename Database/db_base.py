# -*- encoding: utf-8 -*-
__author__ = 'shuhao.wang'

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from . import db_engine
from . import db_session

Base = declarative_base()


def setup():
    db_session.get_session()

    Base.metadata.create_all(db_engine.get_engine())

__all__ = ("setup")