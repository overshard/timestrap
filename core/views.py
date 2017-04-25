# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from datetime import timedelta, date

from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.db.models import Sum

from .admin import EntryResource
from .models import Timesheet, Task, Entry


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['timesheets'] = Timesheet.objects.all()

        entries_per_timesheet = []
        for timesheet in context['timesheets'].iterator():
            entries_per_timesheet.append(
                Entry.objects.filter(task__timesheet=timesheet).count()
            )
        context['entries_per_timesheet'] = entries_per_timesheet

        time_per_timesheet = []
        for timesheet in context['timesheets'].iterator():
            entries = (Entry.objects
                            .filter(task__timesheet=timesheet)
                            .aggregate(Sum('duration')))
            if entries['duration__sum']:
                total_time = int(entries['duration__sum'].total_seconds()/3600)
            else:
                total_time = 0
            time_per_timesheet.append(total_time)
        context['time_per_timesheet'] = time_per_timesheet

        time_per_day = OrderedDict()
        current_date = date.today()
        one_day = timedelta(days=1)
        seven_days_ago = current_date - timedelta(days=7)
        while current_date > seven_days_ago:
            entries = (Entry.objects
                            .filter(date=seven_days_ago)
                            .aggregate(Sum('duration')))
            if entries['duration__sum']:
                total_time = int(entries['duration__sum'].total_seconds()/3600)
            else:
                total_time = 0
            time_per_day[seven_days_ago] = total_time
            seven_days_ago += one_day
        time_per_day = time_per_day
        context['time_per_day'] = time_per_day

        context['total_tasks'] = Task.objects.count()
        context['total_entries'] = Entry.objects.count()
        total_duration = Entry.objects.aggregate(Sum('duration'))
        # TODO: Make hour conversion of timedelta into function since we use
        # three times in this view alone.
        if total_duration['duration__sum']:
            total_hours = int(total_duration['duration__sum']
                              .total_seconds()/3600)
        else:
            total_hours = 0
        context['total_hours'] = total_hours

        return context


class TimesheetsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/timesheets.html'

    def get_context_data(self, **kwargs):
        context = super(TimesheetsView, self).get_context_data(**kwargs)
        context['timesheets'] = Timesheet.objects.all()
        return context


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


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/reports.html'


@login_required
def entries_csv_export(request):
    dataset = EntryResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="entries.csv"'
    return response
