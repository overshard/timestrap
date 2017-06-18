# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal, ROUND_DOWN

from django.contrib.auth.models import User, Permission

from rest_framework import serializers

from core.models import Client, Project, Entry
from core.fields import DurationField
from core.utils import duration_decimal

from core.models import Task, Invoice


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username',)


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'url', 'name', 'codename',)


class ClientProjectSerializer(serializers.HyperlinkedModelSerializer):
    total_entries = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()
    percent_done = serializers.SerializerMethodField()
    estimate = DurationField(required=False)

    class Meta:
        model = Project
        fields = ('id', 'url', 'name', 'client', 'estimate', 'total_entries',
                  'total_duration', 'percent_done',)

    def get_total_entries(self, obj):
        return obj.get_total_entries()

    def get_total_duration(self, obj):
        return obj.get_total_duration()

    def get_percent_done(self, obj):
        return obj.get_percent_done()


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    projects = ClientProjectSerializer(many=True, read_only=True)
    total_projects = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'url', 'name', 'payment_id', 'invoice_email',
                  'archive', 'projects', 'total_projects', 'total_duration',)

    def get_total_projects(self, obj):
        return obj.get_total_projects()

    def get_total_duration(self, obj):
        return obj.get_total_duration()


class ProjectClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'url', 'name',)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    client_details = ProjectClientSerializer(source='client', read_only=True)
    total_entries = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()
    percent_done = serializers.SerializerMethodField()
    estimate = DurationField(required=False)

    class Meta:
        model = Project
        fields = ('id', 'url', 'client', 'client_details', 'name',
                  'archive', 'estimate', 'total_entries', 'total_duration',
                  'percent_done',)

    def get_queryset(self):
        queryset = super(ProjectSerializer, self).get_queryset()
        return queryset.filter(archive=False)

    def get_total_entries(self, obj):
        return obj.get_total_entries()

    def get_total_duration(self, obj):
        return obj.get_total_duration()

    def get_percent_done(self, obj):
        return obj.get_percent_done()


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'url', 'name', 'hourly_rate',)


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    duration = DurationField()
    project_details = ProjectSerializer(source='project', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    task_details = TaskSerializer(source='task', read_only=True)

    class Meta:
        model = Entry
        fields = ('id', 'url', 'project', 'project_details', 'task',
                  'task_details', 'user', 'user_details', 'date', 'duration',
                  'note', 'invoiced',)


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    client_details = ProjectClientSerializer(source='client', read_only=True)
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ('id', 'url', 'client', 'client_details', 'amount', 'entries',
                  'created', 'paid', 'transaction_id',)

    def get_amount(self, obj):
        total = Decimal('0.00')
        for entry in obj.entries.iterator():
            total += Decimal(
                duration_decimal(entry.duration) * entry.task.hourly_rate)
        return total.quantize(Decimal('.01'), rounding=ROUND_DOWN)
