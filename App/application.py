# -*- encoding:utf-8 -*-
__author__="shuhao.wang"

import sys
import os
import copy


class Application(object):
    def __init__(self, *args, **kwargs):
        self.app_name = kwargs['app_name'] if "app_name" in kwargs else "Desire"
        self.args = copy.deepcopy(args)
        self.kwargs = copy.deepcopy(kwargs)
        if 'app_name' in self.kwargs:
            del self.kwargs['app_name']

        self.app_entry = None
        self._init()

    def _init(self):
        sys.path.append(os.getcwd())

        setting = __import__("setting.settings")
        settings = setting.settings

    def start(self):
        if self.app_entry:
            self.app_entry(*self.args, **self.kwargs)
        pass
    pass