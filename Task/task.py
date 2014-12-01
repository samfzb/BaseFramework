# -*- encoding: utf-8 -*-

import threading

from Desire.BaseFramework.Database import db_session

from .models import ModelTask, ModelSubTask
from .error import *
from . import worker


STATE_SUCCESS = 0
STATE_FAILED = -1
STATE_INITIAL = -2
STATE_START = -3
STATE_IN_PROGRESS = -4
STATE_IN_STOP = -5
STATE_FINISH = STATE_SUCCESS
STATE_STOPPED = -6


class SubTask(object):
    def __init__(self, parent_task, model=None, worker=None, args=None):
        self.parent_task = parent_task
        self.model = model
        self.worker = worker
        self.args = args

        if self.model is None:
            self._create()

        if self.worker is None:
            self._create_worker()

    def _create(self):
        if self.worker is None:
            raise TaskCreateError("No worker!")

        session = db_session.get_session()
        self.model = ModelSubTask()
        self.model.parent_id = self.parent_task.get_id()
        self.model.state = STATE_INITIAL
        self.model.name = self.worker.__workername__
        self.model.args = self.args
        session.add(self.model)
        session.commit()

    def get_state(self):
        return self.model.state

    def set_state(self, state):
        session = db_session.get_session()
        with session.begin():
            self.model.state = state
            session.add(self.model)

        self._on_state_change()

    def _on_state_change(self):
        global STATE_SUCCESS, STATE_FAILED, STATE_INITIAL, STATE_START, STATE_IN_PROGRESS, \
            STATE_IN_STOP, STATE_FINISH, STATE_STOPPED
        state = self.get_state()
        if state == STATE_FAILED:
            pass
        elif state == STATE_FINISH:
            pass
        elif state == STATE_INITIAL:
            pass
        elif state == STATE_START:
            pass
        elif state == STATE_IN_PROGRESS:
            pass
        elif state == STATE_IN_STOP:
            pass
        elif state == STATE_STOPPED:
            pass
        pass

    def _create_worker(self):
        self.worker = worker.create(self.model.name, self.args)

    def handle_fail(self):
        self.parent_task.handle_fail(self)

    def handle_finish(self):
        self.parent_task.handle_finish(self)

    def resume(self):
        self.worker.resume()

    def handle_start(self):
        try:
            state = self.get_state()
            self.set_state(state)
        except:
            self.set_state(STATE_FAILED)

    def handle_stopped(self):

        pass

    def start(self):
        try:
            state = self.get_state()
            self.set_state(state)
        except:
            self.set_state(STATE_FAILED)

    def stop(self):
        self.set_state(STATE_IN_STOP)


class TaskManager(object):
    def __init__(self):
        self.tasks = {}
        self.tasks_mutex = threading.Lock()
        self.session = None
        try:
            self._load()
        except:
            raise TaskLoadError("TaskManage load task error")

    def _load(self):
        session = db_session.get_session(autocommit=False)
        self.session = session
        tasks = session.query(ModelTask).filter(ModelTask.state != STATE_SUCCESS)

        for task in tasks:
            self.tasks[task.id] = Task(task)

    def create(self):
        task = Task()
        self.tasks_mutex.acquire()
        self.tasks[task.get_id()] = task
        self.tasks_mutex.release()

    def get(self, task_id):
        self.tasks_mutex.acquire()
        task = self.tasks.get(task_id, None)
        self.tasks_mutex.release()
        if task == None:
            session = db_session.get_session()
            task_model = session.query(ModelTask).filter(ModelTask.id == task_id)
            task = Task(task_model)

        return task


class Task(object):
    def __init__(self, model=None):
        self.model = model
        self.session = db_session.get_session(autocommit=False)
        if self.model is None:
            self._create()

        self.job_list_mutex = threading.Lock()
        self.job_list = []
        self.wait_event = threading.Event()
        self.wait_event.clear()

    def _create(self):
        new_task = ModelTask()

        new_task.state = STATE_INITIAL
        new_task.type = 0

        session = self.session
        session.add(new_task)
        session.flush()
        session.commit()

        self.model = new_task
        self.session = session

    def get_id(self):
        return self.model.id if self.model else 0

    def set_type(self, type):
        self.model.type = type
        self.session.flush()
        self.session.commit()

    def get_type(self):
        return self.model.type if self.model else 0

    def start(self):
        for job in self.job_list:
            job.start()

    def stop(self):
        for job in self.job_list:
            job.stop()

    def finish(self):
        self.model.state = STATE_FINISH
        self.session.flush()
        self.session.commit()

    def handle_sub_task_fail(self, sub_task):
        if sub_task in self.job_list:
            pass
        pass

    def handle_sub_task_finish(self, sub_task):
        pass

    def create_sub_task(self, worker, worker_args=None):
        sub_task = SubTask(self, worker, worker_args)
        pass
