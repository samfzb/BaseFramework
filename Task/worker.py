# -*- encoding: utf-8 -*-

import threading


from .error import *


WORKER_CLS_MUTEX = threading.Lock()
WORKER_CLS = {}


def register(cls):
    global WORKER_CLS, WORKER_CLS_MUTEX
    WORKER_CLS_MUTEX.acquire()
    WORKER_CLS[cls.__workername__] = cls
    WORKER_CLS_MUTEX.release()


def create(cls_name, args):
    global WORKER_CLS
    try:
        return WORKER_CLS[cls_name](args)
    except:
        raise WorkerCreateError("Class %s not exist" % cls_name)


class Worker(object):
    __workername__ = 'worker'

    def __init__(self, task, args=None):
        self.args = args
        self.task = task

    def __str__(self):
        return self.__workername__

    def start(self):
        try:
            self.on_start()
        except:
            self.handle_failure()

    def resume(self):
        try:
            self.on_resume()
        except:
            self.handle_failure()

    def finish(self):
        try:
            self.on_finish()
        except:
            self.handle_failure()

    def stop(self):
        self.on_stop()

    def handle_failure(self):
        try:
            self.on_failure()
        except:
            pass
        self.task.handle_failure()

    def handle_finish(self):
        try:
            self.on_finish()
            self.task.handle_finish()
        except:
            pass

        pass

    def on_start(self):
        raise NotImplementedError("Method on_start does not implemented")

    def on_resume(self):
        raise NotImplementedError("Method on_repair does not implemented")

    def on_failure(self):
        raise NotImplementedError("Method on_failure does not implemented")

    def on_finish(self):
        raise NotImplementedError("Method on_finish was not implemented")

    def on_stop(self):
        raise NotImplementedError("Method on_stop was not implemented")

    def dump(self, format_func=None):
        dump_obj = {
            "name": self.__workername__,
            "args": self.args
        }

        return format_func(dump_obj) if format_func else dump_obj
