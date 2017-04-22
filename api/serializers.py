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
    timesheet_details = TimesheetSerializer(source='timesheet', read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'url', 'timesheet', 'timesheet_details', 'name',)


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    task_details = TaskSerializer(source='task', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Entry
        fields = ('id', 'url', 'task', 'task_details', 'user', 'user_details',
                  'date', 'duration', 'note',)
