# -*- encoding: utf-8 -*-

import json


class Resource(object):
    def __init__(self, *args, **kwargs):
        self.id = kwargs["id"] if "id" in kwargs else None
        self.type = kwargs["type"] if "type" in kwargs else "Resource"
        self.state = None
        self.sub_resources = []
        self.attrs = {}
        self.from_dict(kwargs)

    def __getitem__(self, item):
        if item == "id" or item == "type" or item == 'state':
            return getattr(self, item)

        return self.attrs[item]

    def __setitem__(self, key, value):
        if key == 'id' or key == 'state':
            setattr(self, key, value)
        else:
            self.attrs[key] = value

    def from_dict(self, res_dict):
        if isinstance(res_dict, basestring):
            obj = json.loads(res_dict)
        elif isinstance(res_dict, dict):
            obj = res_dict
        else:
            raise ValueError("Invalid resource: %s" % res_dict)

        if "id" not in obj:
            raise ValueError("an object has no id: %s" % str(obj))

        for key, value in obj.items():
            self[key] = value

        if "sub_res" in obj:
            self.sub_resources = obj["sub_res"]

    def to_dict(self):
        obj = {
            "id": self.id,
            "type": "Resource",
            "state": self.state
        }
        for key, value in self.attrs.items():
            obj[key] = value

        obj["sub_res"] = self.sub_resources

        return obj

    def attach_resource(self, res):
        if res is None:
            raise ValueError("Resource is None")
        if not hasattr(res, "id"):
            raise ValueError("Invalid resource object")

        if res not in self.sub_resources:
            self.sub_resources.append(res.id)

    def detach_resource(self, res):
        if res is None:
            raise ValueError("Resource is None")
        if res in self.sub_resources:
            self.sub_resources.remove(res.id)

    def __cmp__(self, other):
        if isinstance(other, (int, long)):
            return self.id == other
        return self.id == other.id