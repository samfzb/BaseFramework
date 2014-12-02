# -*- encoding: utf-8 -*-

from datetime import datetime

from sqlalchemy import *

from Desire.BaseFramework.Database.db_base import Base


class ModelLogger(Base):
    __tablename__ = "logger"

    id = Column(Integer, primary_key=True, unique=True)

    app_name = Column(String(64))
    level = Column(Integer)
    mod_name = Column(String(64))
    log_time = Column(DateTime, default=datetime.now)
    message = Column(Text)
    __table_args__ = (Index('app_name', 'mod_name', 'log_time'), )
