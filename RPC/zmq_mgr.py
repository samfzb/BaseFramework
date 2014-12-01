# -*- encoding: utf-8 -*-
__author__ = 'shuhao.wang'

import zmq
import threading

_CONTEXT_MUTEX = threading.Lock()
_CONTEXT = None

def zmq_init():
    global _CONTEXT_MUTEX
    global _CONTEXT

    _CONTEXT_MUTEX.acquire()
    if _CONTEXT is None:
        _CONTEXT = zmq.Context()

    _CONTEXT_MUTEX.release()


def zmq_rep_socket(bind="tcp://*:12345", router=False):
    global _CONTEXT

    socket = _CONTEXT.socket(zmq.REP)
    if router:
        socket.connect(bind)
    else:
        socket.bind(bind)

    return socket


def zmq_req_socket(dst_addr="tcp://127.0.0.1:12345"):
    global _CONTEXT

    socket = _CONTEXT.socket(zmq.REQ)
    socket.connect(dst_addr)

    return socket

def set_ident_uuid(socket, ident_uuid):
    socket.set(zmq.IDENTITY, ident_uuid)
