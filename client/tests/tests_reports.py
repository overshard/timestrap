from core.models import Entry

from . import SeleniumTestCase


class ReportsTestCase(SeleniumTestCase):

    def test_reports_navigation(self):
        nav_reports = self.find('nav-reports')
        nav_reports.click()

        self.find('view-reports')

    def test_reports_visible(self):
        self.test_reports_navigation()

        entries = Entry.objects.all()
        for entry in entries:
            entry_id = 'entry-%s' % (entry.id,)
            self.find(entry_id)
