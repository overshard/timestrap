# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, timedelta

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Timesheet, Task, Entry


class TimesheetTestCase(TestCase):
    def setUp(self):
        Timesheet.objects.create(name='Timestrap')

    def test_timesheet_created(self):
        timesheet = Timesheet.objects.get(name='Timestrap')
        self.assertEqual(timesheet.name, 'Timestrap')


class TaskTestCase(TestCase):
    timesheet = None

    def setUp(self):
        self.timesheet = Timesheet.objects.create(name='Timestrap')
        Task.objects.create(timesheet=self.timesheet, name='Testing')

    def test_task_created(self):
        task = Task.objects.get(name='Testing')
        self.assertEqual(task.name, 'Testing')
        self.assertEqual(task.timesheet, self.timesheet)


class EntryTestCase(TestCase):
    task = None
    user = None

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
