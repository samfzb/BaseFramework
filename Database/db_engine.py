# -*- encoding: utf-8 -*-

from sqlalchemy import create_engine


__ENGINE__ = None


def init_engine(conn_string, echo=True):
    global __ENGINE__
    __ENGINE__ = create_engine(conn_string, echo=echo)


def get_engine():
    global __ENGINE__

    if __ENGINE__:
        return __ENGINE__
    else:
        raise SystemError("sqlaclchemy was not initialize!")