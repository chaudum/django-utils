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

    def process_response(self, request, response):
        ## print "SSL_DEBUG: hostname=%s" % get_host(request)
        ## print "SSL_DEBUG: uri=%s" % request.get_full_path()
        if (response.status_code == 302 or response.status_code == 301) and \
                not response["Location"].startswith("http"):

            if response["Location"].startswith("/"):
                ## Redirect location is an absolute path starting with a leading slash
                abs_path = response["Location"]
            else:
                ## Redirect location is a relative path starting with ./ or ../
                abs_path = path.abspath(path.join(request.get_full_path(),response["Location"]))
                if response["Location"].endswith("/"):
                    ## Add a trailing slash if redirect location had one
                    abs_path += "/"

            ## Generate new URL
            newurl = "https://%s%s" % (get_host(request),abs_path)
            ## print "SSL_DEBUG: redirect=%s" % newurl
            return HttpResponsePermanentRedirect(newurl)

        else:
            return response


class MultipleProxyMiddleware:
    """https://docs.djangoproject.com/en/1.3/ref/request-response/"""

    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
    ]

    def process_request(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()
