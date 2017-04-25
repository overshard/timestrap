# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
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

        self.c = Client()

        fake_user = fake.simple_profile()
        fake_password = fake.password()
        User.objects.create_user(fake_user['username'], fake_user['mail'],
                                 fake_password)

        self.c.login(username=fake_user['username'], password=fake_password)

    def test_users_get(self):
        page = self.c.get('/api/users/')
        self.assertEqual(page.status_code, 200)

    def test_timesheets_get(self):
        page = self.c.get('/api/timesheets/')
        self.assertEqual(page.status_code, 200)

    def test_tasks_get(self):
        page = self.c.get('/api/tasks/')
        self.assertEqual(page.status_code, 200)

    def test_entries_get(self):
        page = self.c.get('/api/entries/')
        self.assertEqual(page.status_code, 200)

    def test_timesheets_post(self):
        page = self.c.post('/api/timesheets/', {
            'name': fake.company()
        })
        self.assertEqual(page.status_code, 201)

    def test_timesheets_post_unicode(self):
        page = self.c.post('/api/timesheets/', {
            'name': 'Юникод'
        })
        self.assertEqual(page.status_code, 201)

    def test_tasks_post(self):
        timesheets_page = self.c.get('/api/timesheets/')
        timesheets = timesheets_page.json()

        page = self.c.post('/api/timesheets/', {
            'timesheet': timesheets['results'][0]['url'],
            'name': fake.job()
        })

        self.assertEqual(page.status_code, 201)

    def test_tasks_post_unicode(self):
        timesheets_page = self.c.get('/api/timesheets/')
        timesheets = timesheets_page.json()

        page = self.c.post('/api/timesheets/', {
            'timesheet': timesheets['results'][0]['url'],
            'name': 'Юникод'
        })

        self.assertEqual(page.status_code, 201)

    def test_entries_post(self):
        tasks_page = self.c.get('/api/tasks/')
        tasks = tasks_page.json()
        users_page = self.c.get('/api/users/')
        users = users_page.json()

        page = self.c.post('/api/entries/', {
            'task': tasks['results'][0]['url'],
            'user': users['results'][0]['url'],
            'duration': '1:30:00'
        })

        self.assertEqual(page.status_code, 201)
