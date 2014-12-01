# -*- encoding: utf-8 -*-

_RES_CLASS_MAP = {}

def init_class(res_map):
    global _RES_CLASS_MAP
    _RES_CLASS_MAP = res_map.copy()


def create(cls_name, *args, **kwargs):
    if cls_name is None or cls_name == "":
        raise ValueError("Invalid class name")

    if cls_name in _RES_CLASS_MAP:
        return _RES_CLASS_MAP[cls_name](*args, **kwargs)

    raise LookupError("Can not found class: %s" % cls_name)
