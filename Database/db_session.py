# -*- encoding: utf-8 -*-

import threading

from sqlalchemy.orm import sessionmaker, scoped_session

from . import db_engine


SESSION_MUTEX = threading.Lock()

SESSION_AUTO_COMMIT = None
SESSION_MANUAL_COMMIT = None

def get_session(autocommit=True, expire_on_commit=False):
    global SESSION_AUTO_COMMIT, SESSION_MANUAL_COMMIT
    global SESSION_MUTEX

    SESSION_MUTEX.acquire()
    session = SESSION_AUTO_COMMIT if autocommit else SESSION_MANUAL_COMMIT

    if session is None:
        session = scoped_session(sessionmaker(bind=db_engine.get_engine(),
                               autocommit=autocommit,
                               expire_on_commit=expire_on_commit))
        if autocommit:
            SESSION_AUTO_COMMIT = session
        else:
            SESSION_MANUAL_COMMIT = session

    SESSION_MUTEX.release()
    return session()