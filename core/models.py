# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import User


class Timesheet(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return 'Timesheet: ' + self.name


class Task(models.Model):
    timesheet = models.ForeignKey(Timesheet, related_name='tasks')
    name = models.CharField(max_length=255)

    def __str__(self):
        return 'Task: ' + self.name


class Entry(models.Model):
    task = models.ForeignKey(Task, related_name='entries')
    user = models.ForeignKey(User, related_name='entries')
    date = models.DateField(blank=True)
    duration = models.DurationField(blank=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Entries'

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = date.today()
        super(Entry, self).save(*args, **kwargs)

    def __str__(self):
        return 'Entry for ' + self.task.name

    def parse_duration(self, duration):
        hours = None
        minutes = None

        if duration.isdigit():
            hours = int(duration)
        elif ':' in duration:
            duration_split = duration.split(':')
            hours = int(duration_split[0])
            minutes = int(duration_split[1])
        elif '.' in duration:
            duration_split = duration.split('.')
            hours = int(duration_split[0])
            minutes = int(60 * float('.' + duration_split[1]))

        if hours or minutes:
            self.duration = timedelta(hours=hours, minutes=minutes)
        else:
            raise ValueError('Could not parse duration.')
