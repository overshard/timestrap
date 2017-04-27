from django.conf.urls import url

from .views import (DashboardView, ReportsView, ClientsView, EntriesView,
                    entries_csv_export)


urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^reports/$', ReportsView.as_view(), name='reports'),
    url(r'^reports/export/$', entries_csv_export, name='reports-export'),
    url(r'^clients/$', ClientsView.as_view(), name='clients'),
    url(r'^entries/$', EntriesView.as_view(), name='entries'),
]
