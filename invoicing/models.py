# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Invoice(models.Model):
    client = models.ForeignKey('timesheets.Client')
    entries = models.ManyToManyField('timesheets.Entry')
    date = models.DateField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
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
            else:
                total += entry.duration * self.hourly_rate
        return total


class Task(models.Model):
    name = models.CharField(max_length=255)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2,
                                      blank=True, null=True)

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return 'Task: ' + self.name
