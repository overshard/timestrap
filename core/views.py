# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .admin import EntryResource
from .models import Timesheet, Task, Entry


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['timesheets'] = Timesheet.objects.all()

        entries_per_timesheet = []
        for timesheet in context['timesheets']:
            entries_per_timesheet.append(
                Entry.objects.filter(task__timesheet=timesheet).count()
            )
        context['entries_per_timesheet'] = entries_per_timesheet

        time_per_timesheet = []
        for timesheet in context['timesheets']:
            entries = Entry.objects.filter(task__timesheet=timesheet)
            total_time = timedelta()
            for entry in entries:
                total_time += entry.duration
            total_time = int(total_time.total_seconds()/3600)
            time_per_timesheet.append(total_time)
        context['time_per_timesheet'] = time_per_timesheet

        return context


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


def entries_csv_export(request):
    dataset = EntryResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="entries.csv"'
    return response
