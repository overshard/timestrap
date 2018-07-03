from django.contrib.auth.models import User
from django.test import TestCase

from .models import Conf, Site, SitePermission


class ConfTestCase(TestCase):

    def test_conf_created(self):
        site = Site.objects.create(domain='test.site', name='Test Site')
        self.assertIsInstance(site.conf, Conf)


class SitePermissionTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('Test User', 'test@user.com',
                                             'test')
        Site.objects.create(domain='test1.site', name='Test Site 1')
        Site.objects.create(domain='test2.site', name='Test Site 2')

    def test_sitepermission_created(self):
        site_permission = SitePermission.objects.create(user=self.user)
        self.assertIsInstance(site_permission, SitePermission)

    def test_sitepermission_sites_added(self):
        site_permission = SitePermission.objects.create(user=self.user)
        site_permission.sites.set(Site.objects.all())
        site_permission.save()
        self.assertQuerysetEqual(site_permission.sites.all(),
                                 map(repr, Site.objects.all()))
