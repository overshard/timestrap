# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.forms import PasswordResetForm

from conf.models import Site
from conf.utils import current_site_id


class TimestrapPasswordResetForm(PasswordResetForm):
    """
    Override the 'domain' and 'site_name' email context variables to use the
    current site.
    """
    def save(self, **kwargs):
        site = Site.objects.get(id=current_site_id())
        kwargs['extra_email_context'] = {
            'domain': site.domain,
            'site_name': site.name,
        }
        super(TimestrapPasswordResetForm, self).save(**kwargs)
