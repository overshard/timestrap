from __future__ import division

from .middleware import current_request


def current_site_id():
    """
    Return the ID of the current Site.
    """
    request = current_request()
    site = getattr(request, 'site', None)
    site_id = getattr(site, 'id', None)
    return site_id
