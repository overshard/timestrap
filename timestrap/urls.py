from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views

from .forms import TimestrapPasswordResetForm


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(
        '^password_reset/$',
        views.PasswordResetView.as_view(form_class=TimestrapPasswordResetForm),
        name='password_reset',
    ),

    url('^', include('django.contrib.auth.urls')),

    url(r'', include('core.urls')),
    url(r'', include('api.urls')),
]
