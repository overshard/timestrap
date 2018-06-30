from datetime import timedelta, datetime

from django.contrib.auth.models import User

from selenium.common.exceptions import NoSuchElementException

from . import SeleniumTestCase

from ..models import Entry, Project, Task
from ..utils import parse_duration


class EntriesTestCase(SeleniumTestCase):

    def test_entries_navigation(self):
        nav_timesheet = self.find('nav-timesheet')
        nav_timesheet.click()

        self.find('view-timesheet')

    def test_entries_visible(self):
        self.test_entries_navigation()

        entries = Entry.objects.filter(user=User.objects.get(username='admin'))
        for entry in entries:
            entry_id = 'entry-%s' % (entry.id,)
            self.find(entry_id)

    def test_entries_add(self):
        self.test_entries_navigation()

        tracker_project = self.find('tracker-project')
        tracker_task = self.find('tracker-task')
        tracker_note = self.find('tracker-note')
        tracker_duration = self.find('tracker-duration')

        project = Project.objects.first()
        task = Task.objects.first()

        self.select(project.name, tracker_project)
        self.select(task.name, tracker_task)
        tracker_note.send_keys('new entry note')
        tracker_duration.send_keys('3:50')

        # Submit button only shows up after duration is entered
        tracker_submit = self.find('tracker-submit')
        tracker_submit.click()

        # TODO: Find the entry and not the view?
        view_timesheet = self.find('view-timesheet')
        self.contains(project.name, view_timesheet)
        self.contains(task.name, view_timesheet)
        self.contains('new entry note', view_timesheet)
        self.contains('3:50', view_timesheet)

        entry = Entry.objects.get(note='new entry note')
        self.assertEqual(entry.note, 'new entry note')
        self.assertEqual(entry.duration, timedelta(hours=3, minutes=50))

    def test_entries_delete(self):
        self.test_entries_navigation()

        entry = Entry.objects.filter(user=User.objects.get(username='admin')).first()  # noqa: E501
        entry_id = 'entry-%s' % (entry.id,)
        entry_element = self.find(entry_id)
        entry_menu = self.find('entry-menu', entry_element)
        entry_menu_delete = self.find('entry-menu-delete', entry_element)

        entry_menu.click()
        entry_menu_delete.click()

        self.assertRaises(NoSuchElementException, self.find, entry_id)
        self.assertRaises(Task.DoesNotExist, Task.objects.get, id=entry.id)

    def test_entries_change(self):
        # TODO: This is incomplete, need to test select fields and date
        self.test_entries_navigation()

        entry = Entry.objects.filter(user=User.objects.get(username='admin')).first()  # noqa: E501
        entry_id = 'entry-%s' % (entry.id,)
        entry_element = self.find(entry_id)
        entry_menu = self.find('entry-menu', entry_element)
        entry_menu_change = self.find('entry-menu-change', entry_element)

        entry_menu.click()
        entry_menu_change.click()

        entry_modal_date = self.find('entry-modal-date')
        entry_modal_project = self.find('entry-modal-project')
        entry_modal_task = self.find('entry-modal-task')
        entry_modal_note = self.find('entry-modal-note')
        entry_modal_duration = self.find('entry-modal-duration')
        entry_modal_submit = self.find('entry-modal-submit')

        cleaned_date = datetime.strptime(
            entry_modal_date.get_attribute('value'),
            '%Y-%m-%d',
        ).date()
        cleaned_project = int(
            entry_modal_project.get_attribute('value').split('/')[-2]
        )
        cleaned_task = int(
            entry_modal_task.get_attribute('value').split('/')[-2]
        )
        cleaned_duration = parse_duration(
            entry_modal_duration.get_attribute('value')
        )

        self.assertEqual(entry.date, cleaned_date)
        self.assertEqual(entry.project.id, cleaned_project)
        self.assertEqual(entry.task.id, cleaned_task)
        self.assertEqual(entry.note, entry_modal_note.get_attribute('value'))
        self.assertEqual(entry.duration, cleaned_duration)

        self.clear(entry_modal_note)
        entry_modal_note.send_keys('new entry note')
        self.clear(entry_modal_duration)
        entry_modal_duration.send_keys('3:50')
        entry_modal_submit.click()

        self.contains('new entry note', entry_element)
        self.contains('3:50', entry_element)

        entry = Entry.objects.get(id=entry.id)
        self.assertEqual(entry.note, 'new entry note')
        self.assertEqual(entry.duration, timedelta(hours=3, minutes=50))
