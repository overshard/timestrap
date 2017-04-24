# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from rest_framework import viewsets
import django_filters

from core.models import Timesheet, Task, Entry
from .serializers import (UserSerializer, TimesheetSerializer, TaskSerializer,
                          EntrySerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TimesheetViewSet(viewsets.ModelViewSet):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer
    filter_fields = ('id',)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_fields = ('id', 'timesheet',)


class EntryFilter(django_filters.rest_framework.FilterSet):
    min_date = django_filters.DateFilter(name="date", lookup_expr="gte")
    max_date = django_filters.DateFilter(name="date", lookup_expr="lte")

    class Meta:
        model = Entry
        fields = ('id', 'date', 'user', 'task', 'task__timesheet',)


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_class = EntryFilter
