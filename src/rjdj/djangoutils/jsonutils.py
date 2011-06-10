# ################################################################################
#
# -*- coding: utf-8 -*-
#
# Created by Christian Haudum on 2011/01/28
# Copyright (c) 2011 by Reality Jockey Ltd.
#
# ################################################################################

__docformat__ = "reStructuredText"


from json import dumps, loads, JSONEncoder
from time import mktime

class ExtendedJSONEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, "timetuple"):
            return int(mktime(o.timetuple()))
        elif hasattr(o, "__dict__"):
            return {'__class__':o.__class__.__name__,
                    'o': o.__dict__,
                    }
        else:
            return str(o)

def json_encode(obj):
    return dumps(obj, cls=ExtendedJSONEncoder)

def json_decode(json):
    return loads(json)
