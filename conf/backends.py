# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied

from .models import Site
from .utils import current_site_id


class SitePermissionBackend(ModelBackend):
    """
    Checks for permission to the current site for the logging in user.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super(SitePermissionBackend, self).authenticate(
            request, username, password, **kwargs)

        if user and user.is_active:
            if user.is_superuser:
                return user

        '''TODO: Decide what to do if sitepermission is not available.'''
        if hasattr(user, 'sitepermission'):
            site = Site.objects.get(id=current_site_id())
            if site in user.sitepermission.sites.all():
                return user
            else:
                '''TODO: Handle in UI with a more verbose message.'''
                raise PermissionDenied

    def get_user(self, user_id):
        return super(SitePermissionBackend, self).get_user(user_id)
