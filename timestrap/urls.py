from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.views.generic import RedirectView

from registration import urls as registration_urls
from core import urls as core_urls
from api import urls as api_urls


urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url="/static/imgs/favicon.ico", permanent=True),
        name="favicon",
    ),
    path("admin/", admin.site.urls),
    path("", include(auth_urls)),
    path("", include(registration_urls)),
    path("", include(core_urls)),
    path("", include(api_urls)),
]
