from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from . import views


# Instead of using a wildcard for our app views we insert them one at a time
# for naming purposes. This is so that users can change urls if they want and
# the change will propagate throughout the site.
urlpatterns = [
    path(
        '',
        RedirectView.as_view(url=reverse_lazy('timesheet'), permanent=False),
        name='dashboard',
    ),

    path(
        'reports/export/',
        views.ReportExportView.as_view(),
        name='reports-export'
    ),

    path('timesheet/', views.AppView.as_view(), name='timesheet'),
    path('clients/', views.AppView.as_view(), name='clients'),
    path('tasks/', views.AppView.as_view(), name='tasks'),
    path('reports/', views.AppView.as_view(), name='reports'),
]
