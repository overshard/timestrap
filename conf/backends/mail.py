# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail.backends.base import BaseEmailBackend

from conf.models import Site
from conf.utils import current_site_id


class EmailBackend(BaseEmailBackend):
    pass
