# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.conf import settings
from django.http.request import split_domain_port


class ConfMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        domain, port = split_domain_port(request.get_host())

        try:
            current_site = Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            current_site = Site.objects.get(id=settings.SITE_ID)

        request.site = current_site

        return self.get_response(request)
