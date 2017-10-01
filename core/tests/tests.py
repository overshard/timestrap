# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from decimal import Decimal

from django.test import TestCase, override_settings
from django.test import Client as HttpClient
from django.contrib.auth.models import User
from django.core.management import call_command

from conf.models import Site, SitePermission
from ..models import Client, Project, Entry, Task
from ..utils import parse_duration, duration_string, duration_decimal

from csv import DictReader

from io import StringIO

from faker import Factory


fake = Factory.create()


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class ViewsTestCase(TestCase):
    def setUp(self):
        call_command('migrate', verbosity=0)
        self.c = HttpClient()

        fake_user = fake.simple_profile()
        fake_password = fake.password()
        user = User.objects.create_user(fake_user['username'],
                                        fake_user['mail'], fake_password)
        site_permission = SitePermission.objects.create(user=user)
        site_permission.sites = Site.objects.filter(id=1)
        site_permission.save()

        self.c.login(username=fake_user['username'], password=fake_password)

    def test_clients_view(self):
        # Test with and without data in the database
        page = self.c.get('/clients/')
        self.assertEqual(page.status_code, 200)

        call_command('fake', verbosity=0, iterations=1)
        page = self.c.get('/clients/')
        self.assertEqual(page.status_code, 200)

    def test_timesheets_view(self):
        # Test with and without data in the database
        page = self.c.get('/timesheet/')
        self.assertEqual(page.status_code, 200)

        call_command('fake', verbosity=0, iterations=1)
        page = self.c.get('/timesheet/')
        self.assertEqual(page.status_code, 200)

    def test_reports_export_view(self):
        page = self.c.get('/reports/export/')
        self.assertEqual(page.status_code, 200)


class ClientTestCase(TestCase):
    def setUp(self):
        call_command('migrate', verbosity=0)

    def test_client_created(self):
        Client.objects.create(name='Timestrap')
        client = Client.objects.get(name='Timestrap')
        self.assertEqual(client.name, 'Timestrap')

    def test_client_created_unicode(self):
        Client.objects.create(name='Юникод')
        client = Client.objects.get(name='Юникод')
        self.assertEqual(client.name, 'Юникод')

    def test_client_site_relationship(self):
        Site.objects.create(domain='test.site', name='Test Site')
        client = Client.objects.create(name='Client on time.strap')
        self.assertEqual(client.sites.get().name, 'Timestrap')
        client = Client.objects.create(name='Client on test.site')
        client.sites = Site.objects.filter(domain='test.site')
        client.save()
        self.assertEqual(client.sites.get().name, 'Test Site')


class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name='Timestrap')
        self.user = User.objects.create_user('testuser', 'test@example.com',
                                             'testpassword')

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

    def test_project_estimate(self):
        project = Project.objects.create(
            client=self.client,
            name='Testing',
            estimate=5000.00
        )
        task = Task.objects.create(
            name='Testing',
            hourly_rate=100.00
        )
        Entry.objects.create(
            project=project,
            user=self.user,
            task=task,
            duration=timedelta(hours=10),
            note='Creating tests for the core app'
        )
        self.assertEqual(project.get_percent_done(), 20)


class EntryTestCase(TestCase):
    def setUp(self):
        call_command('migrate', verbosity=0)
        client = Client.objects.create(name='Timestrap')
        self.project = Project.objects.create(client=client, name='Testing')
        self.user = User.objects.create_user('testuser', 'test@example.com',
                                             'testpassword')

        Entry.objects.create(
            project=self.project,
            user=self.user,
            duration=timedelta(hours=1),
            note='Creating tests for the core app'
        )
        Entry.objects.create(
            project=self.project,
            user=self.user,
            duration=timedelta(hours=2),
            note='Continue creating tests for the core app'
        )

    def test_entry_created(self):
        entry = Entry.objects.get(duration=timedelta(hours=1))
        self.assertEqual(entry.note, 'Creating tests for the core app')
        entries = Entry.objects.filter(
            duration__lte=timedelta(hours=1, minutes=30)
        )
        self.assertEqual(len(entries), 1)

    def test_entry_site_relationship(self):
        site = Site.objects.create(domain='test.site', name='Test Site')
        entry = Entry.objects.get(duration=timedelta(hours=1))
        self.assertEqual(entry.site.name, 'Timestrap')
        entry.site = site
        entry.save()
        self.assertEqual(entry.site.name, 'Test Site')

    def test_parse_duration(self):
        duration = parse_duration('3.25')
        self.assertEqual(duration, timedelta(hours=3, minutes=15))
        duration = parse_duration('2:34')
        self.assertEqual(duration, timedelta(hours=2, minutes=34))
        duration = parse_duration('0:05')
        self.assertEqual(duration, timedelta(hours=0, minutes=5))
        duration = parse_duration('5')
        self.assertEqual(duration, timedelta(hours=5))
        self.assertEqual(None, parse_duration('wut'))

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


class ReportsTestCase(TestCase):
    def setUp(self):
        call_command('migrate', verbosity=0)
        self.c = HttpClient()

        fake_user = fake.simple_profile()
        fake_password = fake.password()
        user = User.objects.create_user(fake_user['username'],
                                        fake_user['mail'], fake_password)
        site_permission = SitePermission.objects.create(user=user)
        site_permission.sites = Site.objects.filter(id=1)
        site_permission.save()

        self.c.login(username=fake_user['username'], password=fake_password)

        call_command('fake', verbosity=0, iterations=1)

    def assert_entries_by_params(self, params):
        url = '/reports/export/?'
        for param, value in params.items():
            url += '{0}={1}&'.format(param, value)
        report = self.c.get(url)
        lines = DictReader(StringIO(report.content.decode('utf-8')))
        for line in lines:
            self.filter_exported_entry(line).delete()
        self.assertFalse(Entry.objects.filter(**params).exists())

    def filter_exported_entry(self, line):
        # TODO: Improve this for better reporting when assertions fail.
        entries = Entry.objects.filter(
            date=line['date'],
            duration=parse_duration(line['duration']),
            note=line['note'],
            project__name=line['project__name'],
            user__username=line['user__username']
        )
        self.assertEqual(len(entries), 1)
        return entries[0]

    def test_export_response(self):
        report = self.c.get('/reports/export/')
        self.assertEqual(report.status_code, 200)
        self.assertEqual(report.get('Content-Type'), 'text/csv')
        self.assertEqual(report.get('Content-Disposition'),
                         'attachment; filename="report.csv"')

    def test_export_all(self):
        report = self.c.get('/reports/export/')
        lines = DictReader(StringIO(report.content.decode('utf-8')))
        for line in lines:
            self.filter_exported_entry(line).delete()
        # The above should have deleted _all_ entries
        self.assertFalse(Entry.objects.all().exists())

    def test_export_formats(self):
        for f in ['csv', 'xls', 'xlsx', 'tsv', 'ods', 'json', 'yaml', 'html']:
            report = self.c.get('/reports/export/?export_format={0}'.format(f))
            self.assertEqual(report.status_code, 200)
            self.assertEqual(report.get('Content-Type'), 'text/{0}'.format(f))

    def test_export_param_project(self):
        self.assert_entries_by_params({'project': Project.objects.first().id})

    def test_export_param_client(self):
        self.assert_entries_by_params(
            {'project__client': Client.objects.first().id})

    def test_export_param_user(self):
        self.assert_entries_by_params({'user': User.objects.first().id})

    def test_export_param_date_range(self):
        dates = sorted([Entry.objects.first().date, Entry.objects.last().date])
        self.assert_entries_by_params({
            'date__gte': str(dates[0]),
            'date__lte': str(dates[1])
        })


class CommandsTestCase(TestCase):
    def setUp(self):
        pass

    def test_fake(self):
        call_command('fake', verbosity=0)
