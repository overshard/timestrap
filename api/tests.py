# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.contrib.auth.models import User


class BrowseableApiTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        User.objects.create_user(self.username, 'test@example.com',
                                 self.password)
        self.c.login(username=self.username, password=self.password)

    def test_timesheets(self):
        page = self.c.get('/api/timesheets/')
        self.assertEqual(page.status_code, 200)

    def test_tasks(self):
        page = self.c.get('/api/tasks/')
        self.assertEqual(page.status_code, 200)

    def test_entries(self):
        page = self.c.get('/api/entries/')
        self.assertEqual(page.status_code, 200)
