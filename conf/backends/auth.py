from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied

from conf.models import Site
from conf.utils import current_site_id


class SitePermissionBackend(ModelBackend):
    """
    Checks for permission to the current site for the logging in user.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)

        if user and user.is_active and hasattr(user, "sitepermission"):
            site = Site.objects.get(id=current_site_id())
            if site in user.sitepermission.sites.all():
                return user
            else:
                messages.error(
                    request,
                    "This account does not have permission to log "
                    "in to {}.".format(request.site),
                    "no_sitepermission",
                )
                raise PermissionDenied

    def get_user(self, user_id):
        return super().get_user(user_id)
