# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from conf.models import Conf, Site, SitePermission


class Command(BaseCommand):
    help = 'Creates an initial Site and User (admin/admin) for Timestrap.'

    def handle(self, *args, **kwargs):
        verbosity = kwargs['verbosity']

        default_site = Site.objects.get(id=1)
        Conf.objects.create(site=default_site)
        default_site.domain = 'time.strap'
        default_site.name = 'Timestrap'
        default_site.save()

        default_user = User.objects.create_user('admin', password='admin')
        default_user.is_superuser = True
        default_user.is_staff = True
        default_user.save()

        site_permission = SitePermission.objects.create(user=default_user)
        site_permission.sites = Site.objects.filter(id=1)
        site_permission.save()

        if verbosity > 0:
            self.stdout.write(
                self.style.SUCCESS('Successfully created initial site.')
            )
