# -*- encoding: utf-8 -*-

from datetime import datetime

from Desire.FrameWork.Database import db_engine
from Desire.FrameWork.Database import db_session

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ModelLogger(Base):
    __tablename__ = "logger"

    id = Column(Integer, primary_key=True, unique=True)

    app_name = Column(String(64))
    level = Column(Integer)
    mod_name = Column(String(64))
    log_time = Column(DateTime, default=datetime.now)
    message = Column(Text)
    __table_args__ = (Index('app_name', 'mod_name', 'log_time'), )


def init():
    db_session.get_session()

    Base.metadata.create_all(db_engine.get_engine())