# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin as BaseSiteAdmin

from .models import Tenant


class TenantInline(admin.StackedInline):
    model = Tenant
    can_delete = False


class SiteAdmin(BaseSiteAdmin):
    inlines = [
        TenantInline,
    ]


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
