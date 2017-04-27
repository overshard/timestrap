# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import Client as HttpClient
from django.contrib.auth.models import User
from django.core.management import call_command
from django.apps import apps

from faker import Factory


fake = Factory.create()


class AppTestCase(TestCase):
    def setUp(self):
        pass

    def test_api_config(self):
        self.assertEqual(apps.get_app_config('api').name, 'api')


class BrowseableApiTestCase(TestCase):
    def setUp(self):
        call_command('fake', verbosity=0, iterations=1)

        self.c = HttpClient()

        fake_user = fake.simple_profile()
        fake_password = fake.password()
        User.objects.create_user(fake_user['username'], fake_user['mail'],
                                 fake_password)

        self.c.login(username=fake_user['username'], password=fake_password)

    def test_users_get(self):
        page = self.c.get('/api/users/')
        self.assertEqual(page.status_code, 200)

    def test_clients_get(self):
        page = self.c.get('/api/clients/')
        self.assertEqual(page.status_code, 200)

    def test_projects_get(self):
        page = self.c.get('/api/projects/')
        self.assertEqual(page.status_code, 200)

    def test_entries_get(self):
        page = self.c.get('/api/entries/')
        self.assertEqual(page.status_code, 200)

    def test_clients_post(self):
        page = self.c.post('/api/clients/', {
            'name': fake.company()
        })
        self.assertEqual(page.status_code, 201)

    def test_clients_post_unicode(self):
        page = self.c.post('/api/clients/', {
            'name': 'Юникод'
        })
        self.assertEqual(page.status_code, 201)

    def test_projects_post(self):
        clients_page = self.c.get('/api/clients/')
        clients = clients_page.json()

        page = self.c.post('/api/clients/', {
            'client': clients['results'][0]['url'],
            'name': fake.job()
        })

        self.assertEqual(page.status_code, 201)

    def test_projects_post_unicode(self):
        clients_page = self.c.get('/api/clients/')
        clients = clients_page.json()

        page = self.c.post('/api/clients/', {
            'client': clients['results'][0]['url'],
            'name': 'Юникод'
        })

        self.assertEqual(page.status_code, 201)

    def test_entries_post(self):
        projects_page = self.c.get('/api/projects/')
        projects = projects_page.json()
        users_page = self.c.get('/api/users/')
        users = users_page.json()

        page = self.c.post('/api/entries/', {
            'project': projects['results'][0]['url'],
            'user': users['results'][0]['url'],
            'duration': '1:30:00'
        })

        self.assertEqual(page.status_code, 201)
