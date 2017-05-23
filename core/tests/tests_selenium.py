# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import management
from django.test import override_settings

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.webdriver import WebDriver

from pyvirtualdisplay import Display

from easyprocess import EasyProcessCheckInstalledError

from faker import Factory

from datetime import timedelta

from time import sleep

from ..models import Client, Project, Entry, Task


fake = Factory.create()


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class SeleniumTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.display = Display(visible=0, size=(1280, 720))
            cls.display.start()
        except EasyProcessCheckInstalledError:
            # Fall back to geckodriver without headless if Xvfb is not
            # available (as is the case on Windows).
            # TODO: Implement a cross-platform headless solution.
            pass

        cls.profile = fake.simple_profile()
        cls.profile['password'] = fake.password()
        super(SeleniumTestCase, cls).setUpClass()
        cls.driver = WebDriver()
        cls.driver.implicitly_wait(10)
        cls.wait_time = 5

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        try:
            cls.display.stop()
        except AttributeError:
            pass

        super(SeleniumTestCase, cls).tearDownClass()

    def find(self, by, value):
        elements = self.driver.find_elements(by, value)
        if len(elements) is 1:
            return elements[0]
        else:
            return elements

    def addPerms(self, perms):
        for codename in perms:
            self.user.user_permissions.add(
                Permission.objects.get(codename=codename))
        sleep(0.25)

    def waitForPresence(self, element):
        return WebDriverWait(self.driver, self.wait_time).until(
            ec.presence_of_element_located(element))

    def waitForText(self, element, text):
        try:
            WebDriverWait(self.driver, self.wait_time).until(
                ec.text_to_be_present_in_element(element, text))
        except TimeoutException:
            # assertIn produces more verbose failure text.
            self.assertIn(text, self.find(*element).text)

    def waitForClickable(self, element):
        """An element becomes "clickable" when it is not disabled. This method
        is useful for waiting on form buttons that have been disabled while
        javascript is doing work."""
        return WebDriverWait(self.driver, self.wait_time).until(
            ec.element_to_be_clickable(element))

    def select2Select(self, id, value):
        """Select a value in a select2 menu. The select element *must* have an
        id attribute in order for this work. Select2 uses the select element id
        to create its container for selections.
        """
        self.find(By.CSS_SELECTOR, '#select2-' + id +
                  '-container + .select2-selection__arrow').click()
        field = self.waitForPresence((By.CLASS_NAME, 'select2-search__field'))
        field.send_keys(value)
        field.send_keys(Keys.RETURN)

    def logIn(self):
        self.user = User.objects.create_user(self.profile['username'],
                                             self.profile['mail'],
                                             self.profile['password'])

        self.driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.find(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(self.profile['username'])
        password_input = self.find(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(self.profile['password'])
        self.find(By.NAME, 'login').click()
        self.waitForPresence((By.TAG_NAME, 'navigation'))

    def test_login_failure(self):
        self.driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.find(By.NAME, 'username')
        username_input.send_keys(self.profile['username'])
        password_input = self.find(By.NAME, 'password')
        password_input.send_keys('incorrect password')
        self.find(By.NAME, 'login').click()
        # Log in failure creates an alert notice.
        self.waitForPresence((By.CSS_SELECTOR, '.alert.alert-danger'))

    def test_clients_access(self):
        self.logIn()
        self.assertNotIn('nav-app-clients', self.find(By.ID, 'nav-app').text)
        self.addPerms(['view_client'])
        self.driver.get(self.live_server_url)
        self.find(By.ID, 'nav-app-clients').click()
        self.waitForPresence((By.CSS_SELECTOR, 'div#main[data-is="clients"]'))

    def test_clients_add(self):
        self.logIn()
        self.addPerms(['view_client'])
        self.driver.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertNotIn('client-add', self.driver.page_source)
        self.addPerms(['add_client'])
        self.driver.refresh()
        self.find(By.NAME, 'client-name').send_keys('Client')
        self.find(By.NAME, 'client-add-submit').click()
        self.waitForPresence((By.TAG_NAME, 'client'))

    def test_clients_change(self):
        Client(name='Client', archive=False).save()
        self.logIn()
        self.addPerms(['view_client'])
        self.driver.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertFalse(self.find(By.NAME, 'client-change').is_enabled())
        self.addPerms(['change_client'])
        self.driver.refresh()
        self.find(By.NAME, 'client-change').click()
        self.waitForPresence((By.NAME, 'client-name'))
        self.find(By.NAME, 'client-name').send_keys(' Changed')
        self.find(By.NAME, 'client-save').click()
        self.waitForText((By.TAG_NAME, 'client'), 'Client Changed')

    def test_projects_access(self):
        Client(name='Client', archive=False).save()
        self.logIn()
        self.addPerms(['view_client'])
        self.driver.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertNotIn('client-view-projects', self.driver.page_source)
        self.addPerms(['view_project'])
        self.driver.refresh()
        self.waitForPresence((By.CLASS_NAME, 'client-view-projects'))

    def test_projects_add(self):
        Client(name='Client', archive=False).save()
        self.logIn()
        self.addPerms(['view_client', 'view_project'])
        self.driver.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertNotIn('project-add', self.driver.page_source)
        self.addPerms(['add_project'])
        self.driver.refresh()
        self.find(By.CLASS_NAME, 'client-view-projects').click()
        self.waitForPresence((By.NAME, 'project-add'))
        self.find(By.NAME, 'project-name').send_keys('Project')
        self.find(By.NAME, 'project-estimate').send_keys('1')
        self.find(By.NAME, 'project-add-submit').click()
        self.waitForPresence((By.TAG_NAME, 'project'))

    def test_projects_change(self):
        client = Client(name='Client', archive=False)
        client.save()
        Project(name='Project', client=client, estimate=timedelta(hours=1),
                archive=False).save()
        self.logIn()
        self.addPerms(['view_client', 'view_project'])
        self.driver.get('%s%s' % (self.live_server_url, '/clients/'))

        self.find(By.CLASS_NAME, 'client-view-projects').click()
        self.assertFalse(self.find(By.NAME, 'project-change').is_enabled())
        self.addPerms(['change_project'])
        self.driver.refresh()
        self.find(By.CLASS_NAME, 'client-view-projects').click()
        self.waitForPresence((By.NAME, 'project-change'))
        self.find(By.NAME, 'project-change').click()
        self.waitForPresence((By.NAME, 'project-name'))
        self.find(By.NAME, 'project-name').send_keys(' Changed')
        self.find(By.NAME, 'project-estimate').send_keys('.5')
        self.find(By.NAME, 'project-save').click()
        self.waitForText((By.TAG_NAME, 'project'), 'Project Changed')

    def test_tasks_access(self):
        self.logIn()
        self.assertNotIn('nav-app-tasks', self.driver.page_source)
        self.addPerms(['view_task'])
        self.driver.get(self.live_server_url)
        self.find(By.ID, 'nav-app-tasks').click()
        self.waitForPresence((By.CSS_SELECTOR, 'div#main[data-is="tasks"]'))

    def test_tasks_add(self):
        self.logIn()
        self.addPerms(['view_task'])
        self.driver.get('%s%s' % (self.live_server_url, '/tasks/'))

        self.assertNotIn('task-add', self.driver.page_source)
        self.addPerms(['add_task'])
        self.driver.refresh()
        self.waitForPresence((By.NAME, 'task-add'))
        self.find(By.NAME, 'task-name').send_keys('Task')
        self.find(By.NAME, 'task-hourly-rate').send_keys('25')
        self.find(By.NAME, 'task-add-submit').click()
        self.waitForPresence((By.TAG_NAME, 'task'))

    def test_tasks_change(self):
        Task(name='Task', hourly_rate=25).save()
        self.logIn()
        self.addPerms(['view_task'])
        self.driver.get('%s%s' % (self.live_server_url, '/tasks/'))

        self.assertFalse(self.find(By.NAME, 'task-change').is_enabled())
        self.addPerms(['change_task'])
        self.driver.refresh()
        self.find(By.NAME, 'task-change').click()
        self.waitForPresence((By.NAME, 'task-name'))
        self.find(By.NAME, 'task-name').send_keys(' Changed')
        self.find(By.NAME, 'task-hourly-rate').clear()
        self.find(By.NAME, 'task-hourly-rate').send_keys('125')
        self.find(By.NAME, 'task-save').click()
        self.waitForText((By.TAG_NAME, 'task'), 'Task Changed\n$125')

    def test_timesheet_access(self):
        self.logIn()
        self.assertNotIn('nav-app-timesheet', self.driver.page_source)
        self.addPerms(['view_entry'])
        self.driver.get(self.live_server_url)
        self.find(By.ID, 'nav-app-timesheet').click()
        self.waitForPresence((By.CSS_SELECTOR, 'div#main[data-is="entries"]'))

    def test_timesheet_entry_add(self):
        client = Client(name='Client', archive=False)
        client.save()
        Project(name='Project 1', estimate=timedelta(hours=1), client=client,
                archive=False).save()
        Project(name='Project 2', estimate=timedelta(hours=1), client=client,
                archive=False).save()
        Task(name='Task 1', hourly_rate=130).save()
        Task(name='Task 2', hourly_rate=80).save()
        self.logIn()
        self.addPerms(['view_client', 'view_entry',
                       'view_project', 'view_task'])
        self.driver.get('%s%s' % (self.live_server_url, '/timesheet/'))

        self.assertNotIn('entry-add', self.driver.page_source)
        self.addPerms(['add_entry'])
        self.driver.refresh()
        self.select2Select('entry-task', 'Task 2')
        self.select2Select('entry-project', 'Project 1')
        self.find(By.NAME, 'entry-note').send_keys('Note')
        self.find(By.NAME, 'entry-duration').send_keys('0:35')
        self.find(By.NAME, 'entry-add-submit').submit()
        self.waitForPresence((By.TAG_NAME, 'entry'))
        self.waitForText((By.TAG_NAME, 'entry'),
                         'Client\nProject 1\nTask 2\nNote\n0:35')

    def test_timesheet_entry_change(self):
        client = Client(name='Client', archive=False)
        client.save()
        project = Project(name='Project 1', estimate=timedelta(hours=1),
                          client=client, archive=False)
        project.save()
        Project(name='Project 2', estimate=timedelta(hours=1), client=client,
                archive=False).save()
        task = Task(name='Task 1', hourly_rate=130)
        task.save()
        Task(name='Task 2', hourly_rate=80).save()
        # Log in to establish self.user.
        self.logIn()
        Entry(project=project, task=task, user=self.user, note='Note',
              duration=timedelta(minutes=35)).save()
        self.addPerms(['view_client', 'view_entry',
                       'view_project', 'view_task'])
        self.driver.get('%s%s' % (self.live_server_url, '/timesheet/'))

        self.assertNotIn('entry-menu', self.driver.page_source)
        self.addPerms(['change_entry'])
        self.driver.refresh()
        self.find(By.NAME, 'entry-menu').click()
        self.waitForPresence((By.CLASS_NAME, 'entry-menu-change'))
        self.find(By.CLASS_NAME, 'entry-menu-change').click()
        self.waitForPresence((By.NAME, 'entry-save'))
        # self.select2Select('entry-task', 'Task 2')
        self.select2Select('entry-project', 'Project 2')
        self.find(By.NAME, 'entry-note').clear()
        self.find(By.NAME, 'entry-note').send_keys('Changed note')
        self.find(By.NAME, 'entry-duration').clear()
        self.find(By.NAME, 'entry-duration').send_keys('1.5')
        self.find(By.NAME, 'entry-save').click()
        self.waitForPresence((By.TAG_NAME, 'entry'))
        self.waitForText((By.TAG_NAME, 'entry'),
                         'Client\nProject 2\nTask 1\nChanged note\n1:30')

    def test_timesheet_entry_restart(self):
        client = Client(name='Client', archive=False)
        client.save()
        project = Project(name='Project 1', estimate=timedelta(hours=1),
                          client=client, archive=False)
        project.save()
        task = Task(name='Task 1', hourly_rate=130)
        task.save()
        # Log in to establish self.user.
        self.logIn()
        Entry(project=project, task=task, user=self.user, note='Note',
              duration=timedelta(minutes=35)).save()
        self.addPerms(['view_entry', 'change_entry'])
        self.driver.get('%s%s' % (self.live_server_url, '/timesheet/'))

        self.assertNotIn('entry-menu', self.driver.page_source)
        self.addPerms(['change_entry'])
        self.driver.refresh()
        self.find(By.NAME, 'entry-menu').click()
        self.waitForPresence((By.CLASS_NAME, 'entry-menu-restart'))
        self.find(By.CLASS_NAME, 'entry-menu-restart').click()
        self.waitForPresence((By.NAME, 'entry-duration'))
        # Click the "Stop" button and wait for the edit form to appear.
        self.find(By.NAME, 'entry-save').click()
        self.waitForPresence((By.NAME, 'entry-note'))
        self.find(By.NAME, 'entry-save').click()
        # The actual time should not change because the timer does not run for
        # more than 60 seconds.
        self.waitForText((By.TAG_NAME, 'entry'),
                         'Client\nProject 1\nTask 1\nNote\n0:35')

    def test_timesheet_entry_delete(self):
        client = Client(name='Client', archive=False)
        client.save()
        project = Project(name='Project 1', estimate=timedelta(hours=1),
                          client=client, archive=False)
        project.save()
        task = Task(name='Task 1', hourly_rate=130)
        task.save()
        # Log in to establish self.user.
        self.logIn()
        Entry(project=project, task=task, user=self.user, note='Note',
              duration=timedelta(minutes=35)).save()
        self.addPerms(['view_entry', 'delete_entry'])
        self.driver.get('%s%s' % (self.live_server_url, '/timesheet/'))

        self.find(By.NAME, 'entry-menu').click()
        self.waitForPresence((By.CLASS_NAME, 'entry-menu-delete'))
        self.find(By.CLASS_NAME, 'entry-menu-delete').click()
        self.assertNotIn('entry', self.find(By.CLASS_NAME, 'entry-rows').text)

    def test_reports_access(self):
        self.logIn()

        self.find(By.ID, 'nav-app-reports').click()
        self.waitForPresence((By.CSS_SELECTOR, 'div#main[data-is="reports"]'))

    def test_reports_filter(self):
        management.call_command('loaddata', 'tests_data.json', verbosity=0)

        self.logIn()
        self.addPerms(['view_client', 'view_entry',
                       'view_project', 'view_task'])
        self.driver.get('%s%s' % (self.live_server_url, '/reports/'))
        self.waitForPresence((By.CSS_SELECTOR, 'div#main[data-is="reports"]'))

        # The test data contains 12 fake entries.
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry-row')), 12)

        # The "tester" user entered eight of the entries.
        self.select2Select('report-filter-user', 'tester')
        self.find(By.ID, 'generate-report').submit()
        # The "Generate Report" button is disabled while the report is loading.
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry-row')), 8)

        # Four entries from Tester for "Client 1".
        self.select2Select('report-filter-client', 'Client 1')
        self.find(By.ID, 'generate-report').click()
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry-row')), 4)

        # Three entries from tester for "Project 1"
        self.select2Select('report-filter-project', 'Project 1')
        self.find(By.ID, 'generate-report').click()
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry-row')), 3)

        # Two entries from tester for "Task 1"
        self.select2Select('report-filter-task', 'Task 1')
        self.find(By.ID, 'generate-report').click()
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry-row')), 2)

        # Clear existing filters
        self.driver.refresh()
        self.waitForClickable((By.ID, 'generate-report'))
        self.select2Select('report-filter-user', 'tester')

        # Five entries from Tester since 2017-05-06.
        self.find(By.ID, 'report-filter-min-date').click()
        self.waitForPresence((By.CLASS_NAME, 'picker--focused'))
        self.find(By.CSS_SELECTOR, 'div[data-pick="1494043200000"]')[0].click()
        self.find(By.ID, 'generate-report').submit()
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry-row')), 5)

        # Two entries from Tester between 2017-05-06 and 2017-05-16
        self.find(By.ID, 'report-filter-max-date').click()
        self.waitForPresence((By.CLASS_NAME, 'picker--focused'))
        self.find(By.CSS_SELECTOR, 'div[data-pick="1494820800000"]')[1].click()
        self.find(By.ID, 'generate-report').submit()
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry-row')), 2)

        management.call_command('flush', verbosity=0, interactive=False)
