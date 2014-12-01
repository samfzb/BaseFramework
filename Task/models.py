# -*- encoding: utf-8 -*-

from datetime import datetime

from Desire.BaseFramework.Database import db_engine
from Desire.BaseFramework.Database import db_session

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class ModelTask(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, unique=True)

    # 任务类型，由应用自定义
    type = Column(Integer)
    # 当前任务的最后状态
    state = Column(Integer)

    created_time = Column(DateTime, default=datetime.now)
    lasted_time = Column(DateTime, default=datetime.now)

    sub_tasks = relationship("sub_tasks", backref="sub_tasks")


class ModelSubTask(Base):
    __tablename__ = "sub_tasks"

    id = Column(Integer, primary_key=True, unique=True)
    parent_id = Column(Integer, ForeignKey('tasks.id'))

    state = Column(Integer)

    name = Column(String(32))
    args = Column(Text)

    timeout = Column(Integer)

    created_time = Column(DateTime, default=datetime.now)
    lasted_time = Column(DateTime, default=datetime.now)

def init():
    db_session.get_session()

    Base.metadata.create_all(db_engine.get_engine())