# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Permission

from rest_framework import serializers

from timesheets.models import Client, Project, Entry
from timesheets.fields import DurationField


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username')


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'url', 'name', 'codename')


class ClientProjectSerializer(serializers.HyperlinkedModelSerializer):
    total_entries = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'url', 'name', 'client', 'total_entries',
                  'total_duration')

    def get_queryset(self):
        queryset = super(ClientProjectSerializer, self).get_queryset()
        return queryset.filter(archive=False)

    def get_total_entries(self, obj):
        return obj.get_total_entries()

    def get_total_duration(self, obj):
        return obj.get_total_duration()


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    projects = ClientProjectSerializer(many=True, read_only=True)
    total_projects = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'url', 'name', 'archive', 'projects', 'total_projects',
                  'total_duration')

    def get_queryset(self):
        queryset = super(ClientSerializer, self).get_queryset()
        return queryset.filter(archive=False)

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

    class Meta:
        model = Project
        fields = ('id', 'url', 'client', 'client_details', 'name',
                  'archive',)

    def get_queryset(self):
        queryset = super(ProjectSerializer, self).get_queryset()
        return queryset.filter(archive=False)


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    duration = DurationField()
    project_details = ProjectSerializer(source='project', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Entry
        fields = ('id', 'url', 'project', 'project_details', 'user',
                  'user_details', 'date', 'duration', 'note',)
