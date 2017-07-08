# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from import_export import resources

from .models import Client, Project, Entry


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'invoice_email', 'payment_id', 'archive',)
    list_editable = ('archive',)
    list_filter = ('archive',)
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'archive',)
    list_editable = ('archive',)
    list_filter = ('client', 'archive',)
    search_fields = ('name', 'client',)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'date', 'duration', 'invoiced',)
    list_editable = ('date', 'duration',)
    list_filter = ('project', 'project__client', 'user', 'date',)
    search_fields = ('project', 'project__client', 'user', 'note',)
    fieldsets = (
        (None, {
            'fields': ('project', 'user',)
        }),
        ('Date Completed and Duration of Project', {
            'fields': ('date', 'duration',)
        }),
        ('Extra', {
            'fields': ('note',)
        }),
    )


class EntryResource(resources.ModelResource):
    class Meta:
        model = Entry
        fields = ('project__name', 'user__username', 'date', 'duration',
                  'note')
