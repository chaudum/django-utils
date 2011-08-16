##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# All Rights Reserved.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

import json
import logging
import hashlib
import base64
import hmac
from datetime import datetime, timedelta
from pprint import pprint
from rjdj.djangoutils.exceptions import *    
from django.conf import settings

class RequestParser(object):
    """ Base class for validating and parsing JSON requests. """

    TIMESTAMP_KEY = "timestamp"
    ALLOWED_TIME_OFFSET = 60 * 5 # seconds
    
    _data = {}
    _required_keys = ()

    def __init__(self, keys):
        self.raw_data = None
        self.message = None
        self._required_keys = keys

    def check_valid_timestamp(self, value):
        """ Returns if the timestamp is within a certain offset from now. """
        try:
            client_utc_ts = datetime.utcfromtimestamp(value)
        except TypeError as te:
            return False
            
        server_utc_ts = datetime.utcnow()
        d = timedelta(seconds = self.ALLOWED_TIME_OFFSET)
        return abs(client_utc_ts - server_utc_ts) <= d

    def parse(self, payload):
        """ Effectively parses the given base64 encoded JSON string. """
        decoded_payload = ""
        try:
            decoded_payload = base64.b64decode(payload["data"])
            if not self.is_verified(decoded_payload, payload["signature"]):
                raise InvalidSignature
            self.message = json.loads(decoded_payload)
            self._data = self.message["data"]
        except InvalidSignature:
            raise InvalidSignature
        except TypeError,e:
            raise ValueError(str(payload))
        except AttributeError,e:
            raise ValueError(str(e))
        except Exception,e:
            raise ValueError(str(e))

        for key in self._required_keys:
            if not key in self._data.keys():
                raise KeyError("Required key '%s' not in POST data" % key)

        self.timestamp = self.message.get("timestamp")
        if not self.check_valid_timestamp(self.timestamp):
            raise InvalidTimestamp()

        self.uid = self.message.get("uid")

        if self.uid is not None and not \
            (isinstance(self.uid, int) or isinstance(self.uid, long)):
            raise InvalidUID
        
    def get(self, key, default=None):
        return self._data.get(key, default)

    def is_verified(self, decoded_data, signature):
        """Verify the signature."""
        expected_sig = hmac.new(settings.SIGNATURE_SECRET, decoded_data, hashlib.sha1).hexdigest()
        return expected_sig == signature
