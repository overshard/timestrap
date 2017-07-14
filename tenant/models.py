# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.dispatch import receiver


class Tenant(models.Model):
    site = models.OneToOneField(Site, related_name='tenant',
                                on_delete=models.CASCADE)
    color = models.CharField(max_length=5, blank=True)


@receiver(post_save, sender=Site)
def create_tenant(sender, instance, created, **kwargs):
    if created:
        Tenant.objects.create(site=instance)


@receiver(post_save, sender=Site)
def save_tenant(sender, instance, **kwargs):
    instance.tenant.save()
