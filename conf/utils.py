from __future__ import division

from .middleware import current_request

from django.conf import settings


def current_site_id():
    """
    Return the ID of the current Site by checking for a Site in the current
    request and falling back on the default ID in Django settings.
    """
    request = current_request()
    site = getattr(request, 'site', None)
    if site:
        site_id = getattr(site, 'id', None)
    else:
        site_id = settings.SITE_ID
    return site_id
