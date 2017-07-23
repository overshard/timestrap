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

    # SMTP settings
    smtp_host = models.CharField(verbose_name='Host', max_length=255,
                                 null=True)
    smtp_user = models.CharField(verbose_name='User', max_length=255,
                                 null=True)
    # TODO: Store and use this securely.
    smtp_password = models.CharField(
        verbose_name='Password',
        help_text='This password is stored in plaintext. Use with caution!',
        max_length=255,
        null=True
    )
    smtp_port = models.PositiveIntegerField(verbose_name='Port', null=True)
    smtp_tls = models.NullBooleanField(verbose_name='Use TLS', null=True)

    class Meta:
        verbose_name = 'Configuration'
        verbose_name_plural = 'Configuration'

    def __str__(self):
        return 'Configuration for {}'.format(self.site.name)


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
