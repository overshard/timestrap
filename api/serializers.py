# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from rest_framework import serializers

from core.models import Client, Project, Entry
from core.fields import DurationField


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username',)


class ClientProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'url', 'name', 'client')

    def get_queryset(self):
        queryset = super(ClientProjectSerializer, self).get_queryset()
        return queryset.filter(archive=False)


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    projects = ClientProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'url', 'name', 'archive', 'projects')

    def get_queryset(self):
        queryset = super(ClientSerializer, self).get_queryset()
        return queryset.filter(archive=False)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)

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
