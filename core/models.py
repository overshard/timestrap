# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.db import models


class Task(models.Model):
    timesheet = models.ForeignKey('Timesheet', related_name='tasks')
    name = models.CharField(max_length=255)
    complete = models.BooleanField(default=False)

    class Meta:
        ordering = ['timesheet', '-id']

    def __str__(self):
        return 'Task: ' + self.name


class Timesheet(models.Model):
    name = models.CharField(max_length=255)
    complete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        created = False
        if self.id:
            created = True
        super(Timesheet, self).save(*args, **kwargs)
        if not created:
            Task.objects.create(name='General', timesheet=self)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return 'Timesheet: ' + self.name


class Entry(models.Model):
    task = models.ForeignKey('Task', related_name='entries')
    user = models.ForeignKey('auth.User', related_name='entries')
    date = models.DateField(blank=True)
    duration = models.DurationField(blank=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date', '-id']
        verbose_name_plural = 'Entries'

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = date.today()
        super(Entry, self).save(*args, **kwargs)

    def __str__(self):
        return 'Entry for ' + self.task.name
