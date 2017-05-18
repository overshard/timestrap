from django.conf.urls import url

from .views import DashboardView, AppView, reports_export


urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard'),

    url(r'^reports/export/$', reports_export, name='reports-export'),

    url(r'^entries/$', AppView.as_view(), name='entries'),
    url(r'^clients/$', AppView.as_view(), name='clients'),
    url(r'^reports/$', AppView.as_view(), name='reports'),
]
