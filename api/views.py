# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Permission

from rest_framework import viewsets, permissions
import django_filters

from timesheets.models import Client, Project, Entry
from .serializers import (UserSerializer, ClientSerializer,
                          PermissionSerializer, ProjectSerializer,
                          EntrySerializer)
from .pagination import LimitOffsetPaginationWithTotals


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Prevent rest_framework from checking for the "view" perm.
        return (permissions.IsAuthenticated(),)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def get_permissions(self):
        # Prevent rest_framework from checking for the "view" perm.
        return (permissions.IsAuthenticated(),)

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Permission.objects.all()
        else:
            queryset = Permission.objects.filter(user=self.request.user)
        return queryset


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_fields = ('id',)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_fields = ('id', 'client',)


class EntryFilter(django_filters.rest_framework.FilterSet):
    min_date = django_filters.DateFilter(name="date", lookup_expr="gte")
    max_date = django_filters.DateFilter(name="date", lookup_expr="lte")

    class Meta:
        model = Entry
        fields = ('id', 'date', 'user', 'project', 'project__client',)


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    pagination_class = LimitOffsetPaginationWithTotals
    filter_class = EntryFilter
