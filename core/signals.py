from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver

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
