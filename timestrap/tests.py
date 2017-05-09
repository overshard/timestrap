# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.webelement import FirefoxWebElement

from pyvirtualdisplay import Display

from easyprocess import EasyProcessCheckInstalledError

from faker import Factory

from timesheets.models import Client, Project


fake = Factory.create()


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class SeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        try:
            display = Display(visible=0, size=(1280, 720))
            display.start()
        except EasyProcessCheckInstalledError:
            # Fall back to geckodriver without headless if Xvfb is not
            # available (as is the case on Windows).
            # TODO: Implement a cross-platform headless solution.
            pass

        cls.profile = fake.simple_profile()
        cls.profile['password'] = fake.password()
        super(SeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.wait_time = 5

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def find(self, by, value):
        elements = self.selenium.find_elements(by, value)
        if len(elements) is 1:
            return elements[0]
        else:
            return elements

    def waitForPresence(self, element):
        return WebDriverWait(self.selenium, self.wait_time).until(
            ec.presence_of_element_located(element))

    def waitForText(self, element, text):
        return WebDriverWait(self.selenium, self.wait_time).until(
            ec.text_to_be_present_in_element(element, text))

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

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))

        username_input = self.find(By.NAME, 'username')
        username_input.send_keys(self.profile['username'])
        password_input = self.find(By.NAME, 'password')
        password_input.send_keys('incorrect password')
        self.find(By.NAME, 'login').click()
        # Log in failure creates an alert notice.
        self.waitForPresence((By.CSS_SELECTOR, '.alert.alert-danger'))

        self.logIn()

    def test_clients(self):
        self.logIn()

        self.assertNotIn('Clients', self.find(By.ID, 'navbarNav').text)
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_client'))
        self.selenium.get(self.live_server_url)
        self.find(By.CSS_SELECTOR, 'a[href="/clients/"]').click()
        self.waitForPresence((By.ID, 'view-clients'))

        # The <clients> tag only has two elements when there is no add form.
        self.assertEqual(len(self.find(By.CSS_SELECTOR, 'clients > *')), 2)
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_client'))
        self.selenium.refresh()
        self.find(By.NAME, 'client-name').send_keys('Client')
        self.find(By.CSS_SELECTOR,
                  'form[name="client-add"] button[type="submit"]').click()
        self.waitForText((By.CSS_SELECTOR, 'client:first-of-type'), 'Client')

        # The client edit button should be disabled for unprivileged users.
        self.assertIsInstance(self.find(
            By.CSS_SELECTOR, 'client button:disabled'), FirefoxWebElement)
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_client'))
        self.selenium.refresh()
        self.find(By.CSS_SELECTOR, 'client button').click()
        self.waitForPresence((By.CSS_SELECTOR, 'client input'))
        self.find(By.CSS_SELECTOR, 'client input').send_keys(' Changed')
        self.find(By.CSS_SELECTOR, 'client button').click()
        self.waitForText((By.CSS_SELECTOR, 'client:first-of-type'),
                         'Client Changed')

        # If Projects are not viewable, the client name will be in a <span>
        # instead of an <a>.
        self.assertIsInstance(self.find(
            By.CSS_SELECTOR, 'client span.text-primary'), FirefoxWebElement)
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_project'))
        self.selenium.refresh()
        self.find(By.CSS_SELECTOR, 'client a.text-primary')

        # The <client> tag only has two elements when there is no Project add
        # form.
        self.assertEqual(len(self.find(By.CSS_SELECTOR, 'client > *')), 2)
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_project'))
        self.selenium.refresh()
        self.find(By.CSS_SELECTOR, 'client i.fa-chevron-circle-down').click()
        self.waitForPresence((By.NAME, 'project-name'))
        self.find(By.NAME, 'project-name').send_keys('Project')
        self.find(By.CSS_SELECTOR,
                  'form[name="project-add"] button[type="submit"]').click()
        self.waitForText((By.CSS_SELECTOR, 'client project'), 'Project')

        # The project edit button should be disabled for unprivileged users.
        self.assertIsInstance(self.find(
            By.CSS_SELECTOR, 'project button:disabled'), FirefoxWebElement)
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_project'))
        self.selenium.refresh()
        self.find(By.CSS_SELECTOR, 'client i.fa-chevron-circle-down').click()
        self.waitForPresence((By.CSS_SELECTOR, 'project button'))
        self.find(By.CSS_SELECTOR, 'project button').click()
        self.waitForPresence((By.CSS_SELECTOR, 'project input'))
        self.find(By.CSS_SELECTOR, 'project input').send_keys(' Changed')
        self.find(By.CSS_SELECTOR, 'project button').click()
        self.waitForText((By.CSS_SELECTOR, 'project:first-of-type'),
                         'Project Changed')

    def test_entries(self):
        self.logIn()

        self.assertNotIn('Entries', self.find(By.ID, 'navbarNav').text)
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_entry'))
        self.selenium.get(self.live_server_url)
        self.find(By.CSS_SELECTOR, 'a[href="/entries/"]').click()
        self.waitForPresence((By.ID, 'view-entries'))

        client = Client(name="Client", archive=False)
        client.save()
        project = Project(name="Project 1", client=client, archive=False)
        project.save()
        project = Project(name="Project 2", client=client, archive=False)
        project.save()

        # The <entries> tag only has three elements when there is no add form.
        self.assertEqual(len(self.find(By.CSS_SELECTOR, 'entries > *')), 3)
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_entry'),
            Permission.objects.get(codename='view_client'),
            Permission.objects.get(codename='view_project'))
        self.selenium.refresh()
        self.find(By.CLASS_NAME, 'select2-selection__arrow').click()
        self.waitForPresence((By.CLASS_NAME, 'select2-search__field'))
        self.find(By.CLASS_NAME,
                  'select2-search__field').send_keys('Project 2')
        self.find(By.CLASS_NAME,
                  'select2-search__field').send_keys(Keys.RETURN)
        self.find(By.CSS_SELECTOR,
                  'entries form input[placeholder="Note"').send_keys('Note')
        self.find(By.CSS_SELECTOR,
                  'entries form input[placeholder="0:00"').send_keys('0:35')
        self.find(By.CSS_SELECTOR,
                  'entries form button[type="submit"]').submit()
        self.waitForText((By.CSS_SELECTOR, 'entry'),
                         'Client\nProject 2\nNote\n0:35')

        # The <entry> tag does not have an Edit button.
        self.assertNotIn('Edit', self.find(By.CSS_SELECTOR, 'entry').text)
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_entry'))
        self.selenium.refresh()
        self.find(By.ID, 'entry-edit-menu').click()
        # The second entry is the "Edit" link option. For some reason there are
        # two <a> elements for each drop down entry and the real one is the
        # second one.
        self.waitForPresence((By.CSS_SELECTOR, '.dropdown-menu a'))
        self.find(By.CSS_SELECTOR,
                  '.dropdown-menu a:nth-of-type(2)')[1].click()
        self.waitForPresence((By.CSS_SELECTOR,
                              'entry .select2-selection__arrow'))
        self.find(By.CSS_SELECTOR, 'entry .select2-selection__arrow').click()
        self.waitForPresence((By.CLASS_NAME, 'select2-search__field'))
        self.find(By.CLASS_NAME,
                  'select2-search__field').send_keys('Project 1')
        self.find(By.CLASS_NAME,
                  'select2-search__field').send_keys(Keys.RETURN)
        self.find(By.CSS_SELECTOR, 'entry input[value="Note"]').clear()
        self.find(By.CSS_SELECTOR,
                  'entry input[value="Note"]').send_keys('Changed note')
        self.find(By.CSS_SELECTOR, 'entry input[value="0:35"]').clear()
        self.find(By.CSS_SELECTOR,
                  'entry input[value="0:35"]').send_keys('1.5')
        self.find(By.CSS_SELECTOR, 'entry button').click()
        self.selenium.refresh()
        self.assertIn('Client\nProject 1\nChanged note\n1:30',
                      self.find(By.CSS_SELECTOR, 'entry').text)

    def test_reports(self):
        self.logIn()

        self.find(By.CSS_SELECTOR, 'a[href="/reports/"]').click()
        self.waitForPresence((By.ID, 'view-reports'))
