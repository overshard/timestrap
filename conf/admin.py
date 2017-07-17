# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin as BaseSiteAdmin

from .models import Conf


class ConfInline(admin.StackedInline):
    model = Conf
    can_delete = False


class SiteAdmin(BaseSiteAdmin):
    inlines = [
        ConfInline,
    ]


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
