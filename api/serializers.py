# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from rest_framework import serializers

from core.models import Timesheet, Task, Entry


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username',)


class TimesheetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Timesheet
        fields = ('id', 'url', 'name',)


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    timesheet = TimesheetSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'url', 'timesheet', 'name',)


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Entry
        fields = ('id', 'url', 'task', 'user', 'date', 'duration', 'note',)
