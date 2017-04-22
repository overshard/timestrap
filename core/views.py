# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import RedirectView, TemplateView

from .models import Timesheet, Task, Entry


class HomeView(RedirectView):
    # TODO: We should have a landing page but for now we will redirect to the
    # login page.
    permanent = False
    query_string = True
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            self.pattern_name = 'entries'
        return super(HomeView, self).get_redirect_url(*args, **kwargs)


class TimesheetsView(TemplateView):
    template_name = 'core/timesheets.html'


class TasksView(TemplateView):
    template_name = 'core/tasks.html'


class EntriesView(TemplateView):
    template_name = 'core/entries.html'
