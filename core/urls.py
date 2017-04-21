from django.conf.urls import url

from .views import HomeView, EntryView


urlpatterns = [
    url(r'^entry/$', EntryView.as_view(), name='entry'),
    url(r'^$', HomeView.as_view(), name='home'),
]
