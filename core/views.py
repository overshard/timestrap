# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from datetime import timedelta, date

from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.db.models import Sum
from django.template.defaultfilters import slugify

from .admin import EntryResource
from .models import Client, Project, Entry


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['clients'] = Client.objects.all()

        context['projects'] = (Project.objects
                                      .exclude(estimate=None)
                                      .filter(archive=False))

        entries_per_client = []
        for client in context['clients'].iterator():
            entries_per_client.append(
                Entry.objects.filter(project__client=client).count()
            )
        context['entries_per_client'] = entries_per_client

        time_per_client = []
        for client in context['clients'].iterator():
            entries = (Entry.objects
                            .filter(project__client=client)
                            .aggregate(Sum('duration')))
            if entries['duration__sum']:
                total_time = int(entries['duration__sum'].total_seconds()/3600)
            else:
                total_time = 0
            time_per_client.append(total_time)
        context['time_per_client'] = time_per_client

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

        context['total_projects'] = Project.objects.count()
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


class AppView(LoginRequiredMixin, TemplateView):
    template_name = 'core/app.html'


@login_required
def reports_export(request):
    query_dict = request.GET.copy()
    filters = {}
    filter_dict = {'min_date': 'date__gte', 'max_date': 'date__lte',
                   'project': 'project', 'project__client': 'project__client',
                   'user': 'user', 'task': 'task'}
    for key in request.GET:
        value = request.GET.get(key)
        if value and key in filter_dict:
            filters[filter_dict[key]] = value

    if filters:
        queryset = Entry.objects.filter(**filters)
        dataset = EntryResource().export(queryset)
    else:
        queryset = Entry.objects.all()
        dataset = EntryResource().export(queryset)

    allowed_formats = ['csv', 'xls', 'xlsx', 'tsv', 'ods', 'json', 'yaml',
                       'html']
    export_format = query_dict.get('export_format', 'csv')
    if export_format not in allowed_formats:
        export_format = 'csv'

    filename = 'report' + slugify(filters) + '.' + export_format

    response = HttpResponse(
        getattr(dataset, export_format),
        content_type='text/' + export_format)
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
        filename
    )
    return response
