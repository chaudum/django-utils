##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# All Rights Reserved.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

from json import dumps
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError

from rjdj.djangoutils.response import (JSONResponseError,
                                       JSONResponseForbidden,
                                       JSONResponse,
                                       )
from rjdj.djangoutils.exceptions import * 
from rjdj.djangoutils.jsonutils import ExtendedJSONEncoder


def validate_request(parser_class, keys):
    """ Validates a request with the given Parser-(Sub)Class. """
    def new_func(func):
        def inner_func(request):
            if request.method == "POST":
                post_data = {}
                post_data["data"] = request.POST.get("data")
                post_data["signature"] = request.POST.get("signature")
                if not (post_data["data"] and post_data["signature"]):
                    return JSONResponseError("No POST data.")
                parser = parser_class(keys)
                try:
                    parser.parse(post_data)
                except ValueError as e:
                    msg = [u"Malformed POST data."]
                    msg = settings.DEBUG and msg.append(e[0]) or msg 
                    return JSONResponseError(msg)
                except KeyError as e:
                    msg = [u"Invalid arguments."]
                    msg = settings.DEBUG and msg.append(e[0]) or msg 
                    return JSONResponseError(msg)
                except InvalidUID as e:
                    return JSONResponseError("Invalid UID.")
                except InvalidSignature as e:
                    return JSONResponseError("Invalid signature.")
                except InvalidTimestamp as e:
                    return JSONResponseError("Invalid timestamp.")
            else:
                return JSONResponseForbidden("No GET allowed.")
            return func(request,parser)
        return inner_func
    return new_func


def json_response(fn):
    def newfn(*args, **kwargs):
        response_data = fn(*args, **kwargs)
        if isinstance(response_data, JSONResponse):
            json_data = response_data.get_contents()
        elif isinstance(response_data, dict):
            json_response = JSONResponse()
            json_response.content.update(response_data)
            json_data = json_response.get_contents()
        else:
            raise TypeError("View does not response a JSONResponse or dict.")
        status_code = json_data.get("response",{}).get("status_code",200)
        if not isinstance(status_code, int):
            status_code = 200
        res = dumps(json_data, cls=ExtendedJSONEncoder, indent=4)
        mime = 'application/json; charset=UTF-8'
        response = HttpResponse(res,
                                status = status_code,
                                mimetype = mime,
                                content_type = mime)
        return response
    return newfn

def profile(fn):
	def newfn(*args,**kwargs):
		import time; _start = time.time()
		res = fn(*args,**kwargs)
		print "%s %dms" % (fn, (time.time()-_start)*1000)
		return res
	return newfn
