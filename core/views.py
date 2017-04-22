# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import RedirectView, TemplateView

from core.models import Timesheet, Task


class HomeView(RedirectView):
    # TODO: We should have a landing page but for now we will redirect to the
    # login page.
    permanent = False
    query_string = True
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            self.pattern_name = 'timesheets'
        return super(HomeView, self).get_redirect_url(*args, **kwargs)


class TimesheetsView(TemplateView):
    template_name = 'core/timesheets.html'


class TasksView(TemplateView):
    template_name = 'core/tasks.html'

    def get_context_data(self, **kwargs):
        context = super(TasksView, self).get_context_data(**kwargs)

        timesheet = self.request.GET.get('timesheet')
        if timesheet:
            context['timesheet'] = Timesheet.objects.get(id=timesheet)

        return context


class EntriesView(TemplateView):
    template_name = 'core/entries.html'

    def get_context_data(self, **kwargs):
        context = super(EntriesView, self).get_context_data(**kwargs)

        task = self.request.GET.get('task')
        timesheet = self.request.GET.get('task__timesheet')
        if task:
            context['task'] = Task.objects.get(id=task)
        if timesheet:
            context['timesheet'] = Timesheet.objects.get(id=timesheet)

        return context
