# -*- encoding: utf-8 -*-

__all__ = ['TaskCancel', 'TaskError', 'TaskLoadError',
           'TaskSaveError', 'TaskCreateError', 'WorkerCreateError']


class TaskCancel(Exception):
    pass


class TaskSaveError(Exception):
    pass


class TaskLoadError(Exception):
    pass


class TaskError(Exception):
    pass


class TaskCreateError(Exception):
    pass


class WorkerCreateError(Exception):
    pass