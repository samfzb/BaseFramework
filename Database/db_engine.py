# -*- encoding: utf-8 -*-

from sqlalchemy import create_engine


_ENGINE = None


def init_engine(conn_string, echo=True):
    global _ENGINE
    _ENGINE = create_engine(conn_string, echo=echo)


def get_engine():
    global _ENGINE

    if _ENGINE:
        return _ENGINE
    else:
        raise SystemError("sqlaclchemy was not initialize!")