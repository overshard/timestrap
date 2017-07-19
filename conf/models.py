# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
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


class SitePermission(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    sites = models.ManyToManyField('sites.Site', blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Site permission'
        verbose_name_plural = 'Site permissions'

    def __str__(self):
        return 'Site permissions for {}'.format(self.user)
