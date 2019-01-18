from django.contrib.sites.models import Site
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from conf.utils import current_site_id


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


@receiver(post_save)
def sync_clients_save(sender, instance, **kwargs):
    """
    Use django channels to sync all our current clients.
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'sync_clients',
        {
            'type': 'sync_clients.save',
            'model': sender.__name__,
        },
    )


@receiver(post_delete)
def sync_clients_delete(sender, instance, **kwargs):
    """
    Use django channels to sync all our current clients.
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'sync_clients',
        {
            'type': 'sync_clients.delete',
            'model': sender.__name__,
        },
    )
