from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from . import views


urlpatterns = [
    path(
        'reports/export/',
        views.ReportExportView.as_view(),
        name='reports-export'
    ),

    path('timesheet/', views.AppView.as_view(), name='timesheet'),
    path('projects/', views.AppView.as_view(), name='projects'),
    path('clients/', views.AppView.as_view(), name='clients'),
    path('tasks/', views.AppView.as_view(), name='tasks'),
    path('reports/', views.AppView.as_view(), name='reports'),
    path(
        '',
        RedirectView.as_view(url=reverse_lazy('timesheet'), permanent=False),
        name='dashboard',
    ),
]
