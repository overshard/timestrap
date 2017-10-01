# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.management.commands import migrate

from conf.models import Conf, Site, SitePermission


class Command(migrate.Command):
    help = 'Creates an initial Site and User (admin/admin) for Timestrap.'

    def handle(self, *args, **kwargs):
        super(Command, self).handle(*args, **kwargs)

        verbosity = kwargs['verbosity']

        default_site = Site.objects.get(id=1)
        Conf.objects.get_or_create(site=default_site)
        if default_site.domain == 'example.com':
            default_site.name = 'Timestrap'
            default_site.save()

        superusers = User.objects.filter(is_superuser=True)
        if len(superusers) == 0:
            default_user = User.objects.create_user('admin', password='admin')
            default_user.is_superuser = True
            default_user.is_staff = True
            default_user.save()
            site_permission = SitePermission.objects.create(user=default_user)
            site_permission.sites = Site.objects.filter(id=1)
            site_permission.save()
