##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# All Rights Reserved.
#
##############################################################################

# -*- coding: utf-8 -*-

import logging

__docformat__ = "reStructuredText"

class InvalidSignature(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidSignature, self).__init__(args, kwargs)
        logging.error("Invalid signature!")

class InvalidTimestamp(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidTimestamp, self).__init__(args, kwargs)
        logging.error("Invalid timestamp!")

class InvalidUID(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidUID, self).__init__(args, kwargs)
        logging.error("Invalid UID!")

