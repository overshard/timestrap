from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls as auth_urls

from .forms import TimestrapPasswordResetForm


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(auth_urls)),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            form_class=TimestrapPasswordResetForm,
        ),
        name='password_reset',
    ),

    path('', include('core.urls')),
    path('', include('api.urls')),
]
