# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import timedelta

from django.contrib.auth.models import User, Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import management
from django.test import override_settings

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from faker import Factory

from conf.models import Site, SitePermission
from ..models import Client, Project, Entry, Task


fake = Factory.create()


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class SeleniumTestCase(StaticLiveServerTestCase):
    fixtures = ['initial_data']

    @classmethod
    def setUpClass(cls):
        cls.profile = fake.simple_profile()
        cls.profile['password'] = fake.password()
        super(SeleniumTestCase, cls).setUpClass()

        # Using saucelabs for CI testing since travis CI is inconsistent while
        # using selenium.
        if os.environ.get('SAUCE_USERNAME', None):
            sauce_username = os.environ['SAUCE_USERNAME']
            sauce_access_key = os.environ['SAUCE_ACCESS_KEY']
            sauce_url = 'http://' + sauce_username + ':' + sauce_access_key + \
                        '@ondemand.saucelabs.com/wd/hub'
            desired_capabilities = {
                'browserName': 'chrome',
                'version': '58',
                'platform': 'ANY',
                'chromeOptions': {
                    'prefs': {
                        'credentials_enable_service': False,
                        'profile': {
                            'password_manager_enabled': False
                        }
                    }
                }
            }
            if os.environ.get('TRAVIS_JOB_NUMBER', None):
                desired_capabilities.update({
                    'tunnel-identifier': os.environ['TRAVIS_JOB_NUMBER'],
                    'build': os.environ['TRAVIS_BUILD_NUMBER'],
                    'tags': [os.environ['TRAVIS_PYTHON_VERSION'], 'CI']
                })
            cls.driver = webdriver.Remote(
                command_executor=sauce_url,
                desired_capabilities=desired_capabilities
            )
        else:
            options = Options()
            if os.environ.get('GOOGLE_CHROME_BINARY', None):
                options.binary_location = os.environ['GOOGLE_CHROME_BINARY']
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--log-level=3')
            options.add_argument('--window-size=1280,720')

            cls.driver = webdriver.Chrome(chrome_options=options)

        cls.driver.implicitly_wait(10)
        cls.wait_time = 5

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

        super(SeleniumTestCase, cls).tearDownClass()

    def setUp(self):
        if type(self.driver) is webdriver.Remote:
            # Provide context to appear in the saucelabs log.
            self.driver.execute_script(
                'sauce:context={0}'.format(self._testMethodName))

    def find(self, by, value):
        elements = self.driver.find_elements(by, value)
        if len(elements) is 1:
            return elements[0]
        else:
            return elements

    def wait(self, seconds):
        """Use a lambda that always returns False to wait for a number of
        seconds without any expected conditions."""
        try:
            WebDriverWait(self.driver, seconds).until(lambda driver: 1 == 0)
        except TimeoutException:
            pass

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
        selector = '#select2-' + id + '-container + .select2-selection__arrow'
        self.waitForClickable((By.CSS_SELECTOR, selector))
        self.find(By.CSS_SELECTOR, selector).click()
        field = self.waitForPresence((By.CLASS_NAME, 'select2-search__field'))
        field.send_keys(value)
        field.send_keys(Keys.RETURN)

    def addPerms(self, perms):
        for codename in perms:
            self.user.user_permissions.add(
                Permission.objects.get(codename=codename))
        self.wait(0.25)

    def logIn(self):
        self.user = User.objects.create_user(self.profile['username'],
                                             self.profile['mail'],
                                             self.profile['password'])

        site_permission = SitePermission.objects.create(user=self.user)
        site_permission.sites = Site.objects.filter(id=1)
        site_permission.save()

        self.driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.find(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(self.profile['username'])
        password_input = self.find(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(self.profile['password'])
        self.find(By.NAME, 'login').click()
        self.waitForPresence((By.ID, 'nav-app'))

    def test_login_failure(self):
        self.driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.find(By.NAME, 'username')
        username_input.send_keys(self.profile['username'])
        password_input = self.find(By.NAME, 'password')
        password_input.send_keys('incorrect password')
        self.find(By.NAME, 'login').click()
        # Log in failure creates an alert notice.
        self.waitForPresence((By.CSS_SELECTOR, '.alert.alert-danger'))

    def test_timer_start(self):
        self.logIn()
        self.waitForPresence((By.ID, 'timer-start'))
        self.find(By.ID, 'timer-start').click()
        self.wait(2)
        self.assertNotIn('0h 0m 0s', self.find(By.ID, 'timer-value').text)

    def test_timer_stop(self):
        self.logIn()
        self.waitForPresence((By.ID, 'timer-start'))
        self.find(By.ID, 'timer-start').click()
        self.wait(2)
        self.find(By.ID, 'timer-stop').click()
        self.assertNotIn('0h 0m 0s', self.find(By.ID, 'timer-value').text)

    def test_timer_reset(self):
        self.logIn()
        self.waitForPresence((By.ID, 'timer-start'))
        self.find(By.ID, 'timer-start').click()
        self.wait(2)
        self.find(By.ID, 'timer-stop').click()
        self.assertNotIn('0h 0m 0s', self.find(By.ID, 'timer-value').text)
        self.find(By.ID, 'timer-reset').click()
        self.waitForText((By.ID, 'timer-value'), '0h 0m 0s')

    def test_clients_access(self):
        self.logIn()
        # self.assertNotIn('nav-app-clients', self.find(By.ID, 'nav-app').text)
        self.addPerms(['view_client'])
        self.driver.get(self.live_server_url)
        self.find(By.ID, 'nav-app-clients').click()
        self.waitForPresence((By.ID, 'client-rows'))

    def test_clients_add(self):
        self.logIn()
        self.addPerms(['view_client'])
        self.driver.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertNotIn('client-add', self.driver.page_source)
        self.addPerms(['add_client'])
        self.driver.refresh()
        self.find(By.NAME, 'client-add').click()
        self.waitForPresence((By.ID, 'client-modal'))
        self.find(By.NAME, 'client-name').send_keys('Client')
        self.find(By.NAME, 'client-email').send_keys('client@company.com')
        self.find(By.NAME, 'client-modal-submit').click()
        self.waitForPresence((By.CLASS_NAME, 'client'))

    def test_clients_change(self):
        Client(name='Client', invoice_email='client@company.com',
               archive=False).save()
        self.logIn()
        self.addPerms(['view_client'])
        self.driver.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertNotIn('client-menu-change', self.driver.page_source)
        self.addPerms(['change_client'])
        self.driver.refresh()
        self.find(By.NAME, 'client-menu').click()
        self.find(By.ID, 'client-menu-change').click()
        self.waitForPresence((By.NAME, 'client-name'))
        self.find(By.NAME, 'client-name').send_keys(' Changed')
        self.find(By.NAME, 'client-modal-submit').click()
        # There is no case insensitive option for this test at present and
        # the driver returns as uppercase because the element also has class
        # text-uppercase.
        self.waitForText((By.CLASS_NAME, 'client-name'), 'CLIENT CHANGED')

    def test_projects_access(self):
        client = Client(name='Client', invoice_email='client@company.com',
                        archive=False)
        client.save()
        Project(name='Project 1', client=client, estimate=timedelta(hours=1),
                archive=False).save()
        self.logIn()
        self.addPerms(['view_client'])
        self.driver.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertNotIn('Project 1', self.driver.page_source)
        self.addPerms(['view_project'])
        self.driver.refresh()
        self.waitForText((By.CLASS_NAME, 'project'), 'Project 1')

    def test_projects_add(self):
        Client(name='Client', invoice_email='client@company.com',
               archive=False).save()
        self.logIn()
        self.addPerms(['view_client', 'view_project'])
        self.driver.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertNotIn('project-add', self.driver.page_source)
        self.addPerms(['add_project'])
        self.driver.refresh()
        self.find(By.NAME, 'project-add').click()
        self.waitForPresence((By.ID, 'project-modal'))
        self.select2Select('project-client', 'Client')
        self.find(By.NAME, 'project-name').send_keys('Project')
        self.find(By.NAME, 'project-estimate').send_keys('1')
        self.find(By.NAME, 'project-modal-submit').click()
        self.waitForPresence((By.CLASS_NAME, 'project'))

    def test_projects_change(self):
        client = Client(name='Client', invoice_email='client@company.com',
                        archive=False)
        client.save()
        Project(name='Project', client=client, estimate=timedelta(hours=1),
                archive=False).save()
        self.logIn()
        self.addPerms(['view_client', 'view_project'])
        self.driver.get('%s%s' % (self.live_server_url, '/clients/'))

        self.assertNotIn('project-menu', self.driver.page_source)
        self.addPerms(['change_project'])
        self.driver.refresh()
        self.waitForClickable((By.NAME, 'project-menu'))
        self.find(By.NAME, 'project-menu').click()
        self.find(By.ID, 'project-menu-change').click()
        self.waitForPresence((By.NAME, 'project-name'))
        self.find(By.NAME, 'project-name').send_keys(' Changed')
        self.find(By.NAME, 'project-estimate').send_keys('.5')
        self.find(By.NAME, 'project-modal-submit').click()
        self.waitForText((By.CLASS_NAME, 'project-name'), 'Project Changed')

    def test_tasks_access(self):
        self.logIn()
        # self.assertNotIn('nav-app-tasks', self.driver.page_source)
        self.addPerms(['view_task'])
        self.driver.get(self.live_server_url)
        self.find(By.ID, 'nav-app-tasks').click()
        self.waitForPresence((By.ID, 'task-rows'))

    def test_tasks_add(self):
        self.logIn()
        self.addPerms(['view_task'])
        self.driver.get('%s%s' % (self.live_server_url, '/tasks/'))

        self.assertNotIn('task-add', self.driver.page_source)
        self.addPerms(['add_task'])
        self.driver.refresh()
        self.find(By.NAME, 'task-add').click()
        self.waitForPresence((By.ID, 'task-modal'))
        self.find(By.NAME, 'task-name').send_keys('Task')
        self.find(By.NAME, 'task-hourly-rate').send_keys('25')
        self.find(By.NAME, 'task-modal-submit').click()
        self.waitForPresence((By.CLASS_NAME, 'task'))

    def test_tasks_change(self):
        Task(name='Task', hourly_rate=25).save()
        self.logIn()
        self.addPerms(['view_task'])
        self.driver.get('%s%s' % (self.live_server_url, '/tasks/'))

        self.assertNotIn('task-menu-change', self.driver.page_source)
        self.addPerms(['change_task'])
        self.driver.refresh()
        self.find(By.NAME, 'task-menu').click()
        self.find(By.ID, 'task-menu-change').click()
        self.waitForPresence((By.NAME, 'task-name'))
        self.find(By.NAME, 'task-name').send_keys(' Changed')
        self.find(By.NAME, 'task-hourly-rate').click()
        self.find(By.NAME, 'task-hourly-rate').clear()
        self.find(By.NAME, 'task-hourly-rate').send_keys('125')
        self.find(By.NAME, 'task-modal-submit').click()
        self.waitForText((By.CLASS_NAME, 'task'), 'Task Changed\n$125')

    def test_timesheet_access(self):
        self.logIn()
        # self.assertNotIn('nav-app-timesheet', self.driver.page_source)
        self.addPerms(['view_entry'])
        self.driver.get(self.live_server_url)
        self.find(By.ID, 'nav-app-timesheet').click()
        self.waitForPresence((By.ID, 'entry-rows'))

    def test_timesheet_entry_add(self):
        client = Client(name='Client', invoice_email='client@company.com',
                        archive=False)
        client.save()
        Project(name='Project 1', estimate=timedelta(hours=1), client=client,
                archive=False).save()
        Project(name='Project 2', estimate=timedelta(hours=1), client=client,
                archive=False).save()
        self.logIn()
        self.addPerms(['view_client', 'view_entry', 'view_project'])
        self.driver.get('%s%s' % (self.live_server_url, '/timesheet/'))

        self.assertNotIn('entry-add', self.driver.page_source)
        self.addPerms(['add_entry'])
        self.driver.refresh()
        self.select2Select('entry-project', 'Project 1')
        self.find(By.NAME, 'entry-note').send_keys('Note')
        self.find(By.NAME, 'entry-duration').send_keys('0:35')
        self.find(By.NAME, 'entry-add-submit').click()
        self.waitForPresence((By.CLASS_NAME, 'entry'))
        self.waitForText((By.CLASS_NAME, 'entry'),
                         'Client\nProject 1\nNote\n0:35')

    def test_timesheet_entry_add_advanced(self):
        client = Client(name='Client', invoice_email='client@company.com',
                        archive=False)
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
        self.find(By.ID, 'entry-advanced-fields').click()
        self.select2Select('entry-task', 'Task 2')
        self.select2Select('entry-project', 'Project 1')
        self.find(By.NAME, 'entry-note').send_keys('Note')
        self.find(By.NAME, 'entry-duration').send_keys('0:35')
        self.find(By.NAME, 'entry-add-submit').click()
        self.waitForPresence((By.CLASS_NAME, 'entry'))
        self.waitForText((By.CLASS_NAME, 'entry'),
                         'Client\nProject 1\nTask 2\nNote\n0:35')

    def test_timesheet_entry_change(self):
        client = Client(name='Client', invoice_email='client@company.com',
                        archive=False)
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
        self.waitForPresence((By.NAME, 'entry-menu'))
        self.find(By.NAME, 'entry-menu').click()
        self.waitForPresence((By.CLASS_NAME, 'entry-menu-change'))
        self.find(By.CLASS_NAME, 'entry-menu-change').click()
        self.waitForPresence((By.NAME, 'entry-save'))
        self.select2Select('entry-project', 'Project 2')
        self.find(By.NAME, 'entry-note').clear()
        self.find(By.NAME, 'entry-note').send_keys('Changed note')
        self.find(By.NAME, 'entry-duration').clear()
        self.find(By.NAME, 'entry-duration').send_keys('1.5')
        self.find(By.NAME, 'entry-save').click()
        self.waitForPresence((By.CLASS_NAME, 'entry'))
        self.waitForText((By.CLASS_NAME, 'entry'),
                         'Client\nProject 2\nTask 1\nChanged note\n1:30')

    def test_timesheet_entry_restart(self):
        client = Client(name='Client', invoice_email='client@company.com',
                        archive=False)
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
        self.addPerms(['view_entry'])
        self.driver.get('%s%s' % (self.live_server_url, '/timesheet/'))

        self.assertNotIn('entry-menu', self.driver.page_source)
        self.addPerms(['change_entry'])
        self.driver.refresh()
        self.waitForPresence((By.NAME, 'entry-menu'))
        self.find(By.NAME, 'entry-menu').click()
        self.waitForPresence((By.CLASS_NAME, 'entry-menu-restart'))
        self.find(By.CLASS_NAME, 'entry-menu-restart').click()
        self.waitForPresence((By.ID, 'timer-stop'))
        # Click Timer's "Stop" button and wait for the save button to appear.
        self.find(By.ID, 'timer-stop').click()
        self.waitForPresence((By.ID, 'timer-entry-save'))
        self.find(By.ID, 'timer-entry-save').click()
        # The actual time should not change because the timer does not run for
        # more than 60 seconds.
        self.waitForText((By.CLASS_NAME, 'entry'),
                         'Client\nProject 1\nTask 1\nNote\n0:35')

    def test_timesheet_entry_delete(self):
        client = Client(name='Client', invoice_email='client@company.com',
                        archive=False)
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

        self.waitForPresence((By.NAME, 'entry-menu'))
        self.find(By.NAME, 'entry-menu').click()
        self.waitForPresence((By.CLASS_NAME, 'entry-menu-delete'))
        self.find(By.CLASS_NAME, 'entry-menu-delete').click()
        self.assertNotIn('entry', self.find(By.ID, 'entry-rows').text)

    def test_reports_access(self):
        self.logIn()
        # self.assertNotIn('nav-app-reports', self.driver.page_source)
        self.addPerms(['view_entry'])
        self.driver.get(self.live_server_url)
        self.find(By.ID, 'nav-app-reports').click()
        self.waitForPresence((By.ID, 'entry-rows'))

    def test_reports_filter(self):
        management.call_command('loaddata', 'test_reports_filter.json', verbosity=0)

        # Log in with the "tester" account, part of the tests data fixture.
        self.driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.find(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys('tester')
        password_input = self.find(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys('tester')
        self.find(By.NAME, 'login').click()
        self.waitForPresence((By.ID, 'nav-app'))

        self.driver.get('%s%s' % (self.live_server_url, '/reports/'))
        self.waitForPresence((By.ID, 'component-reports'))

        # The test data contains 12 fake entries.
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry')), 12)

        # The "tester" user entered eight of the entries.
        self.select2Select('report-filter-user', 'tester')
        self.find(By.ID, 'generate-report').submit()
        # The "Generate Report" button is disabled while the report is loading.
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry')), 8)

        # Four entries from Tester for "Client 1".
        self.select2Select('report-filter-client', 'Client 1')
        self.find(By.ID, 'generate-report').click()
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry')), 4)

        # Three entries from tester for "Project 1"
        self.select2Select('report-filter-project', 'Project 1')
        self.find(By.ID, 'generate-report').click()
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry')), 3)

        # Two entries from tester for "Task 1"
        self.select2Select('report-filter-task', 'Task 1')
        self.find(By.ID, 'generate-report').click()
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry')), 2)

        # Clear existing filters
        self.driver.refresh()
        self.waitForClickable((By.ID, 'generate-report'))
        self.select2Select('report-filter-user', 'tester')

        # Five entries from Tester since 2017-05-06.
        self.find(By.ID, 'report-filter-min-date')

        # Execute Javascript directly using pickadate's odd syntax. Simulated
        # steps to load and click a date on the calendar here would be
        # difficult because the calendar view defaults to the current month.
        self.driver.execute_script(
            "p = $('#report-filter-min-date').pickadate('picker');"
            "p.set('select', [2017, 4, 6]);"
        )
        self.find(By.ID, 'generate-report').submit()
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry')), 5)

        # Three entries from Tester between 2017-05-06 and 2017-05-16
        self.find(By.ID, 'report-filter-max-date')
        self.driver.execute_script(
            "p = $('#report-filter-max-date').pickadate('picker');"
            "p.set('select', [2017, 4, 16]);"
        )
        self.find(By.ID, 'generate-report').submit()
        self.waitForClickable((By.ID, 'generate-report'))
        self.assertEqual(len(self.find(By.CLASS_NAME, 'entry')), 3)

        management.call_command('flush', verbosity=0, interactive=False)
