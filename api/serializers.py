# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from rest_framework import serializers

from core.models import Timesheet, Task, Entry


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff',)


class TimesheetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Timesheet
        fields = '__all__'


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    timesheet = TimesheetSerializer()

    class Meta:
        model = Task
        fields = '__all__'


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Entry
        fields = '__all__'
