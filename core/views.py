# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.models import Timesheet, Task


class HomeView(RedirectView):
    # TODO: We should have a landing page but for now we will redirect to the
    # login page.
    permanent = False
    query_string = True
    pattern_name = 'timesheets'


class TimesheetsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/timesheets.html'


class TasksView(LoginRequiredMixin, TemplateView):
    template_name = 'core/tasks.html'

    def get_context_data(self, **kwargs):
        context = super(TasksView, self).get_context_data(**kwargs)

        timesheet = self.request.GET.get('timesheet')
        if timesheet:
            context['timesheet'] = Timesheet.objects.get(id=timesheet)

        return context


class EntriesView(LoginRequiredMixin, TemplateView):
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
