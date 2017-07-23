# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class I18NMiddleware(MiddlewareMixin):
    """
    Handles the current Site's internationalization settings.
    """
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
