##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# All Rights Reserved.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

from os import path
from django.conf import settings
from django.http import (HttpResponseRedirect,
                         HttpResponsePermanentRedirect,
                         get_host,
                         )


class SSLRedirect:
    """Middleware for SSL"""

    def process_request(self, request):
        pass
#        if settings.DEBUG:
#            print "SSL_DEBUG: hostname=%s" % get_host(request)
#            print "SSL_DEBUG: uri=%s" % request.get_full_path()


    def process_response(self, request, response):
#        if settings.DEBUG:
#            print "SSL_DEBUG: status_code=%s" % response.status_code
        if (response.status_code == 302 or \
            response.status_code == 301) and not \
            response["Location"].startswith("http"):
            if response["Location"].startswith("/"):
                abs_path = response["Location"]
            else:
                abs_path = path.abspath(path.join(request.get_full_path(),response["Location"]))
                if response["Location"].endswith("/"):
                    abs_path += "/"
            newurl = "https://%s%s" % (get_host(request),abs_path)
#            if settings.DEBUG:
#                print "SSL_DEBUG: redirect=%s" % newurl
            return HttpResponsePermanentRedirect(newurl)
        else:
            return response
