# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Timesheet, Task, Entry


@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'timesheet')
    list_filter = ('timesheet',)
    search_fields = ('name', 'timesheet')


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'date', 'duration')
    list_editable = ('date', 'duration')
    list_filter = ('task', 'task__timesheet', 'user', 'date')
    search_fields = ('task', 'task__timesheet', 'user', 'note')
    fieldsets = (
        (None, {
            'fields': ('task', 'user',)
        }),
        ('Date Completed and Duration of Task', {
            'fields': ('date', 'duration',)
        }),
        ('Extra', {
            'fields': ('note',)
        }),
    )
