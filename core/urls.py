from django.conf.urls import url

from .views import (HomeView, TimesheetsView, TasksView, EntriesView,
                    entries_csv_export)


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^timesheets/$', TimesheetsView.as_view(), name='timesheets'),
    url(r'^tasks/$', TasksView.as_view(), name='tasks'),
    url(r'^entries/$', EntriesView.as_view(), name='entries'),
    url(r'^entries/csv/$', entries_csv_export, name='entries_csv_export'),
]
