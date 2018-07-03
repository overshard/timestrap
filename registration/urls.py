from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import TimestrapPasswordResetForm


urlpatterns = [
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            form_class=TimestrapPasswordResetForm,
        ),
        name='password_reset',
    ),
]
