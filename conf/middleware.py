# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import threading

from django.contrib.sites.models import Site
from django.conf import settings
from django.http.request import split_domain_port


_thread_local = threading.local()


def current_request():
    """
    Provides access to the current request at deeper project levels.
    """
    return getattr(_thread_local, 'request', None)


class SiteMiddleware(object):
    """
    Determines the current Site based on the domain in use.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        domain, port = split_domain_port(request.get_host())

        try:
            current_site = Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            current_site = Site.objects.get(id=settings.SITE_ID)

        request.site = current_site
        _thread_local.request = request

        return self.get_response(request)
