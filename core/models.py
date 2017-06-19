# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.db import models
from django.db.models import Sum

from .utils import duration_string


class Client(models.Model):
    name = models.CharField(max_length=255)
    archive = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    invoice_email = models.EmailField(max_length=255, blank=True, null=True)

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['-id']

    def __str__(self):
        return 'Client: ' + self.name

    def get_total_projects(self):
        return self.projects.count()

    def get_total_duration(self):
        return duration_string(self.projects.aggregate(
                Sum('entries__duration')
        )['entries__duration__sum'])


class Project(models.Model):
    client = models.ForeignKey('Client', related_name='projects')
    name = models.CharField(max_length=255)
    archive = models.BooleanField(default=False)
    estimate = models.DurationField(blank=True, null=True)

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['client', '-id']

    def __str__(self):
        return 'Project: ' + self.name

    def get_total_entries(self):
        return self.entries.count()

    def get_total_duration(self):
        return duration_string(self.entries.aggregate(
            Sum('duration')
        )['duration__sum'])

    def get_percent_done(self):
        if self.estimate is not None:
            total_duration = float(self.get_total_duration().split(':')[0])
            total_estimate = \
                float(duration_string(self.estimate).split(':')[0])
            if total_duration != 0 and total_estimate != 0:
                return int(100 * (total_duration/total_estimate))
        return None


class Task(models.Model):
    name = models.CharField(max_length=255)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2,
                                      blank=True, null=True)

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['-id']

    def __str__(self):
        return 'Task: ' + self.name


class Entry(models.Model):
    project = models.ForeignKey('Project', related_name='entries')
    task = models.ForeignKey('core.Task', related_name='entries',
                             blank=True, null=True)
    user = models.ForeignKey('auth.User', related_name='entries')
    date = models.DateField(blank=True)
    duration = models.DurationField(blank=True)
    note = models.TextField(blank=True, null=True)
    invoiced = models.BooleanField(default=False)

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['-date', '-id']
        verbose_name_plural = 'Entries'

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = date.today()
        super(Entry, self).save(*args, **kwargs)

    def __str__(self):
        return 'Entry for ' + self.project.name + ' by ' + self.user.username


class Invoice(models.Model):
    client = models.ForeignKey('Client')  # Redundant with entries?
    entries = models.ManyToManyField('Entry')
    created = models.DateTimeField(auto_now_add=True)
    paid = models.DateTimeField(blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return 'Invoice: ' + self.client.name

    def total_duration(self):
        total = 0
        for entry in self.entries:
            total += entry.duration

    def total_billed(self):
        total = 0
        for entry in self.entries:
            if entry.task.hourly_rate:
                total += entry.duration * entry.hourly_rate
        return total
