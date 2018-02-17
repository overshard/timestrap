# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin as BaseSiteAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Conf, SitePermission


class ConfInline(admin.StackedInline):
    model = Conf
    can_delete = False
    fieldsets = (
        ('Internationalization', {
            'fields': ('i18n_language_code', 'i18n_timezone',)
        }),
        ('Email Settings', {
            'fields': ('smtp_from_address', 'smtp_host', 'smtp_user',
                       'smtp_password', 'smtp_port', 'smtp_tls',)
        }),
    )


class SiteAdmin(BaseSiteAdmin):
    inlines = [
        ConfInline,
    ]


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)


class SitePermissionInline(admin.StackedInline):
    model = SitePermission
    max_num = 1
    can_delete = False


class SitePermissionUserAdmin(UserAdmin):
    UserAdmin.list_filter += ('sitepermission__sites',)
    inlines = [
        SitePermissionInline,
    ]


admin.site.unregister(User)
admin.site.register(User, SitePermissionUserAdmin)
