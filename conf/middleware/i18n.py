# -*- coding: utf-8 -*-
import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from conf.utils import get_site_setting


class I18NMiddleware(MiddlewareMixin):
    """
    Handles the current Site's internationalization settings.
    """
    def process_request(self, request):
        tzname = get_site_setting('i18n_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
