# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from decimal import Decimal

from django.test import TestCase, override_settings
from django.test import Client as HttpClient
from django.contrib.auth.models import User
from django.core.management import call_command

from ..models import Client, Project, Entry
from ..utils import parse_duration, duration_string, duration_decimal

from faker import Factory


fake = Factory.create()


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class ViewsTestCase(TestCase):
    def setUp(self):
        self.c = HttpClient()

        fake_user = fake.simple_profile()
        fake_password = fake.password()
        User.objects.create_user(fake_user['username'], fake_user['mail'],
                                 fake_password)

        self.c.login(username=fake_user['username'], password=fake_password)

    # TODO: Uncomment once verbosity is fixed
    # Forcing verbosity to 0 doesn't seem to work here, disabing till fixed
    # def test_compress(self):
    #     call_command('compress', verbosity=0, force=True)

    def test_dashboard_view(self):
        # Test with and without data in the database
        page = self.c.get('/')
        self.assertEqual(page.status_code, 200)

        call_command('fake', verbosity=0, iterations=1)
        page = self.c.get('/')
        self.assertEqual(page.status_code, 200)

    def test_clients_view(self):
        # Test with and without data in the database
        page = self.c.get('/clients/')
        self.assertEqual(page.status_code, 200)

        call_command('fake', verbosity=0, iterations=1)
        page = self.c.get('/clients/')
        self.assertEqual(page.status_code, 200)

    def test_entries_view(self):
        # Test with and without data in the database
        page = self.c.get('/entries/')
        self.assertEqual(page.status_code, 200)

        call_command('fake', verbosity=0, iterations=1)
        page = self.c.get('/entries/')
        self.assertEqual(page.status_code, 200)

    def test_reports_export_view(self):
        page = self.c.get('/reports/export/')
        self.assertEqual(page.status_code, 200)


class ClientTestCase(TestCase):
    def setUp(self):
        pass

    def test_client_created(self):
        Client.objects.create(name='Timestrap')
        client = Client.objects.get(name='Timestrap')
        self.assertEqual(client.name, 'Timestrap')

    def test_client_created_unicode(self):
        Client.objects.create(name='Юникод')
        client = Client.objects.get(name='Юникод')
        self.assertEqual(client.name, 'Юникод')


class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name='Timestrap')

    def test_project_created(self):
        Project.objects.create(client=self.client, name='Testing')
        project = Project.objects.get(name='Testing')
        self.assertEqual(project.name, 'Testing')
        self.assertEqual(project.client, self.client)

    def test_project_created_unicode(self):
        Project.objects.create(client=self.client, name='Юникод')
        project = Project.objects.get(name='Юникод')
        self.assertEqual(project.name, 'Юникод')
        self.assertEqual(project.client, self.client)


class EntryTestCase(TestCase):
    def setUp(self):
        client = Client.objects.create(name='Timestrap')
        self.project = Project.objects.create(client=client, name='Testing')
        self.user = User.objects.create_user('testuser', 'test@example.com',
                                             'testpassword')
        Entry.objects.create(
            project=self.project,
            user=self.user,
            duration=timedelta(hours=1),
            note='Creating tests for the timesheets app'
        )
        Entry.objects.create(
            project=self.project,
            user=self.user,
            duration=timedelta(hours=2),
            note='Continue creating tests for the timesheets app'
        )

    def test_entry_created(self):
        entry = Entry.objects.get(duration=timedelta(hours=1))
        self.assertEqual(entry.note, 'Creating tests for the timesheets app')
        entries = Entry.objects.filter(
            duration__lte=timedelta(hours=1, minutes=30)
        )
        self.assertEqual(len(entries), 1)

    def test_parse_duration(self):
        duration = parse_duration('3.25')
        self.assertEqual(duration, timedelta(hours=3, minutes=15))
        duration = parse_duration('2:34')
        self.assertEqual(duration, timedelta(hours=2, minutes=34))
        duration = parse_duration('0:05')
        self.assertEqual(duration, timedelta(hours=0, minutes=5))
        duration = parse_duration('5')
        self.assertEqual(duration, timedelta(hours=5))
        with self.assertRaises(ValueError):
            parse_duration('wut')

    def test_duration_string(self):
        duration = duration_string(timedelta(hours=1, minutes=30))
        self.assertEqual(duration, '1:30')
        duration = duration_string(timedelta(hours=3, minutes=2))
        self.assertEqual(duration, '3:02')
        duration = duration_string(None)
        self.assertAlmostEqual(duration, '0:00')

    def test_duration_decimal(self):
        # TODO: Determine is assertAlmostEqual is appropriate here.
        duration = duration_decimal(timedelta(hours=2, minutes=3))
        self.assertAlmostEqual(duration, Decimal(2.05))
        duration = duration_decimal(timedelta(hours=5, minutes=15))
        self.assertAlmostEqual(duration, Decimal(5.25))
        duration = duration_decimal(None)
        self.assertAlmostEqual(duration, Decimal(0))


class CommandsTestCase(TestCase):
    def setUp(self):
        pass

    def test_fake(self):
        call_command('fake', verbosity=0)

    def test_heroku(self):
        call_command('heroku', verbosity=0)
