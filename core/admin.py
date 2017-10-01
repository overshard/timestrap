# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from import_export import resources

from .models import Client, Entry, Project, Task


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_id', 'archive',)
    list_editable = ('archive',)
    list_filter = ('archive', 'sites')
    search_fields = ('name',)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'date', 'duration',)
    list_editable = ('date', 'duration',)
    list_filter = ('project', 'project__client', 'user', 'date', 'site',)
    search_fields = ('project', 'project__client', 'user', 'note',)
    fieldsets = (
        (None, {
            'fields': ('project', 'user',)
        }),
        ('Date Completed & Duration of Project', {
            'fields': ('date', 'duration',)
        }),
        ('Extra', {
            'fields': ('note', 'site',)
        }),
    )


class EntryResource(resources.ModelResource):
    class Meta:
        model = Entry
        fields = ('project__name', 'user__username', 'date', 'duration',
                  'note')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'archive',)
    list_editable = ('archive',)
    list_filter = ('client', 'archive',)
    search_fields = ('name', 'client',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'hourly_rate',)
    list_filter = ('sites',)
    search_fields = ('name',)
