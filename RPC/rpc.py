# -*- encoding: utf-8 -*-
__author__ = 'shuhao.wang'

import threading

from . import zmq_mgr
from . import errors

_SERVICE_ENTRIES = {}
_SERVICE_ENTRIES_MUTEX = threading.Lock()

zmq_mgr.zmq_init()


def _dispatcher(request):
    global _SERVICE_ENTRIES
    global _SERVICE_ENTRIES_MUTEX

    if "method" not in request:
        raise errors.BadRequest("No method name")

    _SERVICE_ENTRIES_MUTEX.acquire()
    entry = _SERVICE_ENTRIES.get(request['method'], None)
    _SERVICE_ENTRIES_MUTEX.release()

    try:
        if entry is None:
            raise errors.MethodNotFound("Method '%s' was not found!" % (request['method']))

        args = request.get('args', None)

        result = entry(*args['args'], **args['kwargs'])
        return {
            "status": True,
            "data": result
        }
    except BaseException as e:
        return {
            "status": False,
            "exception": str(e)
        }


def service(func):
    global _SERVICE_ENTRIES_MUTEX
    global _SERVICE_ENTRIES

    _SERVICE_ENTRIES_MUTEX.acquire()

    name = func.__name__
    if name not in _SERVICE_ENTRIES:
        _SERVICE_ENTRIES[name] = func
    _SERVICE_ENTRIES_MUTEX.release()

    return func


class RPCServer(object):
    def __init__(self, bind, router=False, ident_uuid=None):
        self.socket = zmq_mgr.zmq_rep_socket(bind, router)
        if ident_uuid:
            zmq_mgr.set_ident_uuid(self.socket, ident_uuid)

    def serve_forever(self):
        while True:
            request = self.socket.recv_json()

            result = _dispatcher(request)
            self.socket.send_json(result)


class _Proxy(object):
    def __init__(self, name, client):
        self.name = name
        self.client = client

    def __call__(self, *args, **kwargs):
        request = {
            "method": self.name,
            "args": {
                "args": args,
                "kwargs": kwargs
            }
        }

        response = self.client.call(request)
        if response['status']:
            return response['data']

        raise errors.ServerRaisedError(response['exception'])


class RPCProxy(object):
    def __init__(self, dst, ident_uuid=None):
        self.socket = zmq_mgr.zmq_req_socket(dst)
        if ident_uuid:
            zmq_mgr.set_ident_uuid(self.socket, ident_uuid)

    def __getattr__(self, item):
        return _Proxy(item, self)

    def call(self, request):
        self.socket.send_json(request)
        return self.socket.recv_json()
