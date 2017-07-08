# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.defaultfilters import slugify

from .admin import EntryResource
from .models import Entry


class AppView(LoginRequiredMixin, TemplateView):
    template_name = 'core/app.html'


@login_required
def reports_export(request):
    query_dict = request.GET.copy()
    filters = {}
    filter_dict = {'min_date': 'date__gte', 'max_date': 'date__lte',
                   'project': 'project', 'project__client': 'project__client',
                   'user': 'user', 'task': 'task', 'invoiced': 'invoiced'}
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
