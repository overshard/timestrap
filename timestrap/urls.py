from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('django.contrib.auth.urls')),
    url(r'', include('timesheets.urls')),
    url(r'', include('api.urls')),
]
