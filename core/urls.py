from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from .views import AppView, reports_export


# Instead of using a wildcard for our app views we insert them one at a time
# for naming purposes. This is so that users can change urls if they want and
# the change will propagate throughout the site.
urlpatterns = [
    path(
        '',
        RedirectView.as_view(
            url=reverse_lazy('timesheet'),
            permanent=False,
        ),
        name='dashboard',
    ),

    path('reports/export/', reports_export, name='reports-export'),

    path('timesheet/', AppView.as_view(), name='timesheet'),
    path('clients/', AppView.as_view(), name='clients'),
    path('tasks/', AppView.as_view(), name='tasks'),
    path('reports/', AppView.as_view(), name='reports'),
]
