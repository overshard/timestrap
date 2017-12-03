# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from decimal import Decimal, ROUND_DOWN

from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import duration_string, duration_decimal
from conf.utils import current_site_id
from conf.managers import CurrentSiteManager


@receiver(post_save)
def add_current_site(sender, instance, **kwargs):
    """
    Add the current site to a model's sites property after a save. This is
    required in post save because ManyToManyField fields require an existing
    key.

    TODO: Don't run this on *every* post_save.
    """
    if hasattr(instance, 'sites'):
        if not instance.sites.all():
            instance.sites.set(Site.objects.filter(id=current_site_id()))
            instance.save()


class Client(models.Model):
    name = models.CharField(max_length=255)
    archive = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    sites = models.ManyToManyField(Site)

    objects = models.Manager()
    on_site = CurrentSiteManager()

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
    client = models.ForeignKey('Client', related_name='projects',
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    archive = models.BooleanField(default=False)
    estimate = models.DecimalField(max_digits=10, decimal_places=2,
                                   blank=True, null=True)

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['client', '-id']

    def __str__(self):
        return 'Project: ' + self.name

    def get_total_entries(self):
        return self.entries.count()

    def get_total_cost(self):
        total_cost = Decimal()
        for entry in self.entries.iterator():
            try:
                if entry.task.hourly_rate:
                    total_cost += (
                        duration_decimal(entry.duration)
                        * entry.task.hourly_rate
                    )
            except:  # noqa: E722
                continue
        return total_cost.quantize(Decimal('.01'), rounding=ROUND_DOWN)

    def get_total_duration(self):
        return duration_string(self.entries.aggregate(
            Sum('duration')
        )['duration__sum'])

    def get_percent_done(self):
        if self.estimate is not None:
            total_cost = Decimal(self.get_total_cost())
            total_estimate = Decimal(self.estimate)
            if total_cost != 0 and total_estimate != 0:
                return int(100 * (total_cost/total_estimate))
        return None


class Task(models.Model):
    name = models.CharField(max_length=255)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2,
                                      blank=True, null=True)
    sites = models.ManyToManyField(Site)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['-id']

    def __str__(self):
        return 'Task: ' + self.name


class Entry(models.Model):
    project = models.ForeignKey('Project', related_name='entries',
                                on_delete=models.CASCADE)
    task = models.ForeignKey('core.Task', related_name='entries',
                             blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='entries',
                             on_delete=models.CASCADE)
    date = models.DateField(blank=True)
    duration = models.DurationField(blank=True)
    note = models.TextField(blank=True, null=True)
    site = models.ForeignKey(Site, default=current_site_id(),
                             on_delete=models.CASCADE)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ['-date', '-id']
        verbose_name_plural = 'Entries'

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = date.today()
        if not self.site:
            self.site = Site.objects.get(id=current_site_id())
        super(Entry, self).save(*args, **kwargs)

    def __str__(self):
        return 'Entry for ' + self.project.name + ' by ' + self.user.username
