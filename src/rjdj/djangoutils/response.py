##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# All Rights Reserved.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

import hashlib
import json

class JSONResponse(object):
    """Base class for JSON responses"""

    _INDENT = 4

    status_message = 'success'
    status_code = 200
    uid = -1

    def __init__(self, uid=None, **options):
        self._content = {}
        self.uid = uid or -1
        self._content['uid'] = self.uid
        if options:
            self._content.update(options)

    def get_response(self):
        return {}

    def update_content(self):
        self._content.update(self.get_response())

    @property
    def content(self):
        return self.get_contents()

    def get_contents(self):
        self.update_content()
        resp = {
            'status': self.status_message,
            'status_code': self.status_code,
            'content': self._content,
            }
        return dict(response=resp)

    __dict__ = get_contents

    def __str__(self):
	    return json.dumps(self.get_contents(), indent=self._INDENT)

    def __repr__(self):
        return "<%s status_code=%d\n%s>" % (self.__class__.__name__,
                                            self.status_code,
                                            self.__str__(),
                                            )


class JSONResponseWithMessage(JSONResponse):
    """CAMP response with message array
    base class for error and forbidden response"""

    def __init__(self, msg=None, uid=None):
        ## msg can either be a string or a list of strings
        if msg and not (isinstance(msg, list) or \
                        isinstance(msg, str) or \
                        isinstance(msg, unicode)):
            raise TypeError
        self.message = msg
        super(JSONResponseWithMessage, self).__init__(uid=uid)

    def update_content(self):
        ## we need this because error content is a list instead of a dict
        self._content = self.get_response()

    def get_response(self):
        if isinstance(self.message, list):
            return self.message
        elif isinstance(self.message, str) or \
                 isinstance(self.message, unicode):
            return [self.message,]
        return []


class JSONResponseError(JSONResponseWithMessage):
    """CAMP error response"""

    status_message = 'error'
    status_code = 400


class JSONResponseForbidden(JSONResponseWithMessage):
    """CAMP forbidden response"""

    status_message = 'forbidden'
    status_code = 405
