# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import management
from django.test import override_settings

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

from ..models import Client, Project, Entry


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
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.wait_time = 5

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        try:
            cls.display.stop()
        except AttributeError:
            pass

        super(SeleniumTestCase, cls).tearDownClass()

    def find(self, by, value):
        elements = self.selenium.find_elements(by, value)
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
        return WebDriverWait(self.selenium, self.wait_time).until(
            ec.presence_of_element_located(element))

    def waitForText(self, element, text):
        return WebDriverWait(self.selenium, self.wait_time).until(
            ec.text_to_be_present_in_element(element, text))

    def waitForClickable(self, element):
        """An element becomes "clickable" when it is not disabled. This method
        is useful for waiting on form buttons that have been disabled while
        javascript is doing work."""
        return WebDriverWait(self.selenium, self.wait_time).until(
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

        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.find(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(self.profile['username'])
        password_input = self.find(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(self.profile['password'])
        self.find(By.NAME, 'login').click()
        self.waitForPresence((By.ID, 'view-dashboard'))

    def test_login_failure(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
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
        self.selenium.get(self.live_server_url)
        self.find(By.ID, 'nav-app-clients').click()
        self.waitForPresence((By.ID, 'view-clients'))

    def test_clients_add(self):
        self.logIn()
        self.addPerms(['view_client'])
        self.selenium.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertNotIn('client-add', self.find(By.ID, 'view-clients').text)
        self.addPerms(['add_client'])
        self.selenium.refresh()
        self.find(By.NAME, 'client-name').send_keys('Client')
        self.find(By.NAME, 'client-add-submit').click()
        self.waitForPresence((By.TAG_NAME, 'client'))

    def test_clients_change(self):
        Client(name='Client', archive=False).save()
        self.logIn()
        self.addPerms(['view_client'])
        self.selenium.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertFalse(self.find(By.NAME, 'client-change').is_enabled())
        self.addPerms(['change_client'])
        self.selenium.refresh()
        self.find(By.NAME, 'client-change').click()
        self.waitForPresence((By.NAME, 'client-name'))
        self.find(By.NAME, 'client-name').send_keys(' Changed')
        self.find(By.NAME, 'client-save').click()
        self.waitForText((By.TAG_NAME, 'client'), 'Client Changed')

    def test_projects_access(self):
        Client(name='Client', archive=False).save()
        self.logIn()
        self.addPerms(['view_client'])
        self.selenium.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertNotIn(
            'view-projects', self.find(By.ID, 'view-clients').text)
        self.addPerms(['view_project'])
        self.selenium.refresh()
        self.find(By.ID, 'view-projects')

    def test_projects_add(self):
        Client(name='Client', archive=False).save()
        self.logIn()
        self.addPerms(['view_client', 'view_project'])
        self.selenium.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertNotIn('project-add', self.find(By.TAG_NAME, 'client').text)
        self.addPerms(['add_project'])
        self.selenium.refresh()
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
        self.selenium.get('%s%s' % (self.live_server_url, '/clients/'))

        self.find(By.CLASS_NAME, 'client-view-projects').click()
        self.assertFalse(self.find(By.NAME, 'project-change').is_enabled())
        self.addPerms(['change_project'])
        self.selenium.refresh()
        self.find(By.CLASS_NAME, 'client-view-projects').click()
        self.waitForPresence((By.NAME, 'project-change'))
        self.find(By.NAME, 'project-change').click()
        self.waitForPresence((By.NAME, 'project-name'))
        self.find(By.NAME, 'project-name').send_keys(' Changed')
        self.find(By.NAME, 'project-estimate').send_keys('.5')
        self.find(By.NAME, 'project-save').click()
        self.waitForText((By.TAG_NAME, 'project'), 'Project Changed')

    def test_entries_access(self):
        self.logIn()
        self.assertNotIn('nav-app-entries', self.find(By.ID, 'nav-app').text)
        self.addPerms(['view_entry'])
        self.selenium.get(self.live_server_url)
        self.find(By.ID, 'nav-app-entries').click()
        self.waitForPresence((By.ID, 'view-entries'))

    def test_entries_add(self):
        client = Client(name='Client', archive=False)
        client.save()
        Project(name='Project 1', estimate=timedelta(hours=1), client=client,
                archive=False).save()
        Project(name='Project 2', estimate=timedelta(hours=1), client=client,
                archive=False).save()
        self.logIn()
        self.addPerms(['view_client', 'view_project', 'view_entry'])
        self.selenium.get('%s%s' % (self.live_server_url, '/entries/'))

        self.assertNotIn('entry-add', self.find(By.ID, 'view-entries').text)
        self.addPerms(['add_entry'])
        self.selenium.refresh()
        self.find(By.CLASS_NAME, 'select2-selection__arrow').click()
        self.waitForPresence((By.CLASS_NAME, 'select2-search__field'))
        self.find(By.CLASS_NAME,
                  'select2-search__field').send_keys('Project 1')
        self.find(By.CLASS_NAME,
                  'select2-search__field').send_keys(Keys.RETURN)
        self.find(By.NAME, 'entry-note').send_keys('Note')
        self.find(By.NAME, 'entry-duration').send_keys('0:35')
        self.find(By.NAME, 'entry-add-submit').submit()
        self.waitForText((By.TAG_NAME, 'entry'),
                         'Client\nProject 1\nNote\n0:35')

    def test_entries_change(self):
        client = Client(name='Client', archive=False)
        client.save()
        project = Project(name='Project 1', estimate=timedelta(hours=1),
                          client=client, archive=False)
        project.save()
        Project(name='Project 2', estimate=timedelta(hours=1), client=client,
                archive=False).save()
        # Log in to establish self.user.
        self.logIn()
        Entry(project=project, user=self.user, note='Note',
              duration=timedelta(minutes=35)).save()
        self.addPerms(['view_client', 'view_project', 'view_entry'])
        self.selenium.get('%s%s' % (self.live_server_url, '/entries/'))

        self.assertNotIn('entry-menu', self.find(By.ID, 'view-entries').text)
        self.addPerms(['change_entry'])
        self.selenium.refresh()
        self.find(By.NAME, 'entry-menu').click()
        self.waitForPresence((By.CLASS_NAME, 'entry-menu-change'))
        self.find(By.CLASS_NAME, 'entry-menu-change').click()
        self.waitForPresence((By.NAME, 'entry-save'))
        self.find(By.CSS_SELECTOR, '.select2-selection__arrow').click()
        field = self.waitForPresence((By.CLASS_NAME, 'select2-search__field'))
        field.send_keys('Project 2')
        field.send_keys(Keys.RETURN)
        self.find(By.NAME, 'entry-note').clear()
        self.find(By.NAME, 'entry-note').send_keys('Changed note')
        self.find(By.NAME, 'entry-duration').clear()
        self.find(By.NAME, 'entry-duration').send_keys('1.5')
        self.find(By.NAME, 'entry-save').click()
        self.waitForText((By.TAG_NAME, 'entry'),
                         'Client\nProject 2\nChanged note\n1:30')

    def test_entries_restart(self):
        client = Client(name='Client', archive=False)
        client.save()
        project = Project(name='Project 1', estimate=timedelta(hours=1),
                          client=client, archive=False)
        project.save()
        # Log in to establish self.user.
        self.logIn()
        Entry(project=project, user=self.user, note='Note',
              duration=timedelta(minutes=35)).save()
        self.addPerms(['view_entry', 'change_entry'])
        self.selenium.get('%s%s' % (self.live_server_url, '/entries/'))

        self.assertNotIn('entry-menu', self.find(By.ID, 'view-entries').text)
        self.addPerms(['change_entry'])
        self.selenium.refresh()
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
                         'Client\nProject 1\nNote\n0:35')

    def test_entries_delete(self):
        client = Client(name='Client', archive=False)
        client.save()
        project = Project(name='Project 1', estimate=timedelta(hours=1),
                          client=client, archive=False)
        project.save()
        # Log in to establish self.user.
        self.logIn()
        Entry(project=project, user=self.user, note='Note',
              duration=timedelta(minutes=35)).save()
        self.addPerms(['view_entry', 'delete_entry'])
        self.selenium.get('%s%s' % (self.live_server_url, '/entries/'))

        self.find(By.NAME, 'entry-menu').click()
        self.waitForPresence((By.CLASS_NAME, 'entry-menu-delete'))
        self.find(By.CLASS_NAME, 'entry-menu-delete').click()
        self.assertNotIn('entry', self.find(By.CLASS_NAME, 'entry-rows').text)

    def test_reports_access(self):
        self.logIn()

        self.find(By.ID, 'nav-app-reports').click()
        self.waitForPresence((By.ID, 'view-reports'))

    def test_reports_filter(self):
        management.call_command(
            'loaddata', 'test_reports_data.json', verbosity=0)

        self.logIn()
        self.addPerms(['view_entry'])
        self.selenium.get('%s%s' % (self.live_server_url, '/reports/'))
        self.waitForPresence((By.ID, 'view-reports'))

        # The test data contains 12 fake entries.
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry-row')), 12)

        # The "tester" user entered eight of the entries.
        self.select2Select('report-filter-user', 'tester')
        self.find(By.ID, 'generate-report').submit()
        # The "Generate Report" button is disabled while the report is loading.
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry-row')), 8)

        # Three entries from Tester for "Client 3".
        # TODO: Figure out why this doesn't work. No clients appear in list.
        '''self.select2Select('report-filter-client', '')
        self.find(By.ID, 'generate-report').click()
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry-row')), 3)'''

        # TODO: Add tests for Project filter.

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
