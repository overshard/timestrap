# -*- coding: utf-8 -*-
from django.contrib.sites.managers import CurrentSiteManager as BaseCSM

from .utils import current_site_id


class CurrentSiteManager(BaseCSM):
    """
    Replace the Django CurrentSiteManager to use current_site_id() instead of
    settings.SITE_ID.
    """

    def __init__(self, field_name=None, *args, **kwargs):
        super(BaseCSM, self).__init__(*args, **kwargs)
        self.__field_name = field_name

    def get_queryset(self):
        return super(BaseCSM, self).get_queryset().filter(
            **{self._get_field_name() + '__id': current_site_id()})
