# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.dispatch import receiver


class Conf(models.Model):
    site = models.OneToOneField(Site, related_name='conf',
                                on_delete=models.CASCADE)
    color = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return 'Configuration'


@receiver(post_save, sender=Site)
def create_conf(sender, instance, created, **kwargs):
    if created:
        Conf.objects.create(site=instance)


@receiver(post_save, sender=Site)
def save_conf(sender, instance, **kwargs):
    instance.conf.save()
