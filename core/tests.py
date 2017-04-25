# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.apps import apps

from .models import Timesheet, Task, Entry

from faker import Factory


fake = Factory.create()


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class ViewsTestCase(TestCase):
    def setUp(self):
        self.c = Client()

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

    def test_timesheets_view(self):
        # Test with and without data in the database
        page = self.c.get('/timesheets/')
        self.assertEqual(page.status_code, 200)

        call_command('fake', verbosity=0, iterations=1)
        page = self.c.get('/timesheets/')
        self.assertEqual(page.status_code, 200)

    def test_tasks_view(self):
        # Test with and without data in the database
        page = self.c.get('/tasks/')
        self.assertEqual(page.status_code, 200)

        call_command('fake', verbosity=0, iterations=1)
        page = self.c.get('/tasks/')
        self.assertEqual(page.status_code, 200)

    def test_entries_view(self):
        # Test with and without data in the database
        page = self.c.get('/entries/')
        self.assertEqual(page.status_code, 200)

        call_command('fake', verbosity=0, iterations=1)
        page = self.c.get('/entries/')
        self.assertEqual(page.status_code, 200)

    def test_entries_csv_view(self):
        page = self.c.get('/entries/csv/')
        self.assertEqual(page.status_code, 200)


class AppTestCase(TestCase):
    def setUp(self):
        pass

    def test_core_config(self):
        self.assertEqual(apps.get_app_config('core').name, 'core')


class TimesheetTestCase(TestCase):
    def setUp(self):
        Timesheet.objects.create(name='Timestrap')

    def test_timesheet_created(self):
        timesheet = Timesheet.objects.get(name='Timestrap')
        self.assertEqual(timesheet.name, 'Timestrap')


class TaskTestCase(TestCase):
    def setUp(self):
        self.timesheet = Timesheet.objects.create(name='Timestrap')
        Task.objects.create(timesheet=self.timesheet, name='Testing')

    def test_task_created(self):
        task = Task.objects.get(name='Testing')
        self.assertEqual(task.name, 'Testing')
        self.assertEqual(task.timesheet, self.timesheet)


class EntryTestCase(TestCase):
    def setUp(self):
        timesheet = Timesheet.objects.create(name='Timestrap')
        self.task = Task.objects.create(timesheet=timesheet, name='Testing')
        self.user = User.objects.create_user('testuser', 'test@example.com',
                                             'testpassword')
        Entry.objects.create(
            task=self.task,
            user=self.user,
            duration=timedelta(hours=1),
            note='Creating tests for the core app'
        )
        Entry.objects.create(
            task=self.task,
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

    def test_entry_duration_parser(self):
        # TODO: Flesh this out more, currently only testing one variation of
        # the three supported
        parsed_entry = Entry(
            task=self.task,
            user=self.user
        )
        parsed_entry.parse_duration('3.25')
        parsed_entry.save()
        self.assertEqual(parsed_entry.duration, timedelta(hours=3, minutes=15))


class CommandsTestCase(TestCase):
    def setUp(self):
        pass

    def test_fake(self):
        call_command('fake', verbosity=0)

    def test_heroku(self):
        call_command('heroku', verbosity=0)
