# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import Client as HttpClient
from django.contrib.auth.models import User, Permission
from django.core.management import call_command
from django.apps import apps

from faker import Factory

from conf.models import Site, SitePermission


fake = Factory.create()


def init_api_test_data():
    """
    Generates fake data, starts an HttpClient session, creates a fake user and
    logs that user in.
    """
    call_command('fake', verbosity=0, iterations=1)

    c = HttpClient()

    fake_user = fake.simple_profile()
    fake_password = fake.password()
    user = User.objects.create_user(fake_user['username'], fake_user['mail'],
                                    fake_password)
    site_permission = SitePermission.objects.create(user=user)
    site_permission.sites = Site.objects.filter(id=1)
    site_permission.save()

    user = User.objects.get(username=fake_user['username'])
    c.login(username=fake_user['username'], password=fake_password)

    return [c, user]


class AppTestCase(TestCase):
    def setUp(self):
        pass

    def test_api_config(self):
        self.assertEqual(apps.get_app_config('api').name, 'api')


class ClientBrowseableApiTestCase(TestCase):
    def setUp(self):
        self.c, self.user = init_api_test_data()

    def test_clients_get(self):
        page = self.c.get('/api/clients/')
        self.assertEqual(page.status_code, 403)

        self.user.user_permissions.add(
            Permission.objects.get(codename='view_client'))

        page = self.c.get('/api/clients/')
        self.assertEqual(page.status_code, 200)

    def test_clients_post(self):
        page = self.c.post('/api/clients/', {
            'name': fake.company()
        })
        self.assertEqual(page.status_code, 403)

        self.user.user_permissions.add(
            Permission.objects.get(codename='add_client'))

        page = self.c.post('/api/clients/', {
            'name': fake.company()
        })
        self.assertEqual(page.status_code, 201)

    def test_clients_post_unicode(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_client'))

        page = self.c.post('/api/clients/', {
            'name': 'Юникод'
        })
        self.assertEqual(page.status_code, 201)


class ProjectBrowseableApiTestCase(TestCase):
    def setUp(self):
        self.c, self.user = init_api_test_data()

    def test_projects_get(self):
        page = self.c.get('/api/projects/')
        self.assertEqual(page.status_code, 403)

        self.user.user_permissions.add(
            Permission.objects.get(codename='view_project'))

        page = self.c.get('/api/projects/')
        self.assertEqual(page.status_code, 200)

    def test_projects_post(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_client'))

        clients_page = self.c.get('/api/clients/')
        clients = clients_page.json()

        page = self.c.post('/api/projects/', {
            'client': clients[0]['url'],
            'name': fake.job()
        })

        self.assertEqual(page.status_code, 403)

        self.user.user_permissions.add(
            Permission.objects.get(codename='add_project'))

        page = self.c.post('/api/projects/', {
            'client': clients[0]['url'],
            'name': fake.job()
        })

        self.assertEqual(page.status_code, 201)

    def test_projects_post_unicode(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_project'),
            Permission.objects.get(codename='view_client'))

        clients_page = self.c.get('/api/clients/')
        clients = clients_page.json()

        page = self.c.post('/api/projects/', {
            'client': clients[0]['url'],
            'name': 'Юникод'
        })

        self.assertEqual(page.status_code, 201)


class EntryBrowseableApiTestCase(TestCase):
    def setUp(self):
        self.c, self.user = init_api_test_data()

    def test_entries_get(self):
        page = self.c.get('/api/entries/')
        self.assertEqual(page.status_code, 403)

        self.user.user_permissions.add(
            Permission.objects.get(codename='view_entry'))

        page = self.c.get('/api/entries/')
        self.assertEqual(page.status_code, 200)

    def test_entries_post(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_project'))

        projects_page = self.c.get('/api/projects/')
        projects = projects_page.json()
        users_page = self.c.get('/api/users/')
        users = users_page.json()

        page = self.c.post('/api/entries/', {
            'project': projects[0]['url'],
            'user': users[0]['url'],
            'duration': '1:30:00'
        })

        self.assertEqual(page.status_code, 403)

        self.user.user_permissions.add(
            Permission.objects.get(codename='add_entry'))

        page = self.c.post('/api/entries/', {
            'project': projects[0]['url'],
            'user': users[0]['url'],
            'duration': '1:30:00'
        })

        self.assertEqual(page.status_code, 201)


class UserBrowseableApiTestCase(TestCase):
    def setUp(self):
        self.c, self.user = init_api_test_data()

    def test_permission_get(self):
        page = self.c.get('/api/permissions/')
        self.assertEqual(page.status_code, 200)


class PermissionBrowseableApiTestCase(TestCase):
    def setUp(self):
        self.c, self.user = init_api_test_data()

    def test_users_get(self):
        page = self.c.get('/api/users/')
        self.assertEqual(page.status_code, 200)
