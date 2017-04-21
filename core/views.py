# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import RedirectView, TemplateView

from .models import Timesheet, Task, Entry


class HomeView(RedirectView):
    # TODO: We should have a landing page but for now we will redirect to the
    # login page.
    permanent = False
    query_string = True
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            self.pattern_name = 'entry'
        return super(HomeView, self).get_redirect_url(*args, **kwargs)


class EntryView(TemplateView):
    template_name = 'core/entry.html'

    def get_context_data(self, **kwargs):
        context = super(EntryView, self).get_context_data(**kwargs)
        context['timesheets'] = Timesheet.objects.all()
        context['tasks'] = Task.objects.all()
        context['entries'] = Entry.objects.all()
        return context
