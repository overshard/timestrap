from django.conf.urls import url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from .views import AppView, reports_export


# Instead of using a wildcard for our app views we insert them one at a time
# for naming purposes. This is so that users can change urls if they want and
# the change will propagate throughout the site.
urlpatterns = [
    url(r'^reports/export/$', reports_export, name='reports-export'),

    url(r'^timesheet/$', AppView.as_view(), name='timesheet'),
    url(r'^clients/$', AppView.as_view(), name='clients'),
    url(r'^tasks/$', AppView.as_view(), name='tasks'),
    url(r'^reports/$', AppView.as_view(), name='reports'),

    url(
        r'^$',
        RedirectView.as_view(url=reverse_lazy('timesheet'), permanent=False),
        name='dashboard'
    ),
]
