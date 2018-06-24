from pytz import all_timezones

from django.conf import settings
from django.conf.global_settings import LANGUAGES
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.dispatch import receiver


class Conf(models.Model):
    site = models.OneToOneField(
        Site,
        related_name='conf',
        on_delete=models.CASCADE
    )

    # Internationalization settings
    i18n_language_code = models.CharField(
        verbose_name='Language Code',
        max_length=7,
        choices=LANGUAGES,
        default=settings.LANGUAGE_CODE
    )
    i18n_timezone = models.CharField(
        verbose_name='Timezone',
        max_length=255,
        choices=(zip(all_timezones, all_timezones)),
        default=settings.TIME_ZONE
    )

    # SMTP settings
    smtp_from_address = models.EmailField(
        verbose_name='"From" Email Address',
        default=settings.DEFAULT_FROM_EMAIL,
        blank=True
    )
    smtp_host = models.CharField(
        verbose_name='SMTP Host',
        max_length=255,
        blank=True,
        default=settings.EMAIL_HOST
    )
    smtp_user = models.CharField(
        verbose_name='SMTP Username',
        max_length=255,
        blank=True,
        default=settings.EMAIL_HOST_USER
    )
    # TODO: Store and use this securely.
    smtp_password = models.CharField(
        verbose_name='SMTP Password',
        help_text='This password is stored in plaintext. Use with caution!',
        max_length=255,
        blank=True,
        default=settings.EMAIL_HOST_PASSWORD
    )
    smtp_port = models.PositiveIntegerField(
        verbose_name='SMTP Port',
        blank=True,
        default=settings.EMAIL_PORT
    )
    smtp_tls = models.BooleanField(
        verbose_name='Use TLS',
        default=settings.EMAIL_USE_TLS
    )

    objects = models.Manager()

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
