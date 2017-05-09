# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.webelement import FirefoxWebElement

from pyvirtualdisplay import Display

from faker import Factory


fake = Factory.create()


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class SeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        display = Display(visible=0, size=(1280, 720))
        display.start()

        cls.profile = fake.simple_profile()
        cls.profile['password'] = fake.password()
        super(SeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def logIn(self):
        self.user = User.objects.create_user(self.profile['username'],
                                             self.profile['mail'],
                                             self.profile['password'])

        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(self.profile['username'])
        password_input = self.selenium.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(self.profile['password'])
        self.selenium.find_element_by_name('login').click()
        self.selenium.find_element_by_id('view-dashboard')

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))

        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys(self.profile['username'])
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('incorrect password')
        self.selenium.find_element_by_name('login').click()
        # Log in failure creates an alert notice.
        self.selenium.find_element_by_css_selector('.alert.alert-danger')

        self.logIn()

    def test_clients(self):
        self.logIn()

        self.assertNotIn('Clients', self.selenium.find_element_by_css_selector(
            '#navbarNav').text)
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_client'))
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_css_selector(
            'a[href="/clients/"]').click()
        self.selenium.find_element_by_id('view-clients')

        # The <clients> tag only has two elements when there is no add form.
        self.assertEqual(len(self.selenium.find_elements_by_css_selector(
            'clients > *')), 2)
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_client'))
        self.selenium.refresh()
        self.selenium.find_element_by_name('client-name').send_keys('Client')
        self.selenium.find_element_by_css_selector(
            'form[name="client-add"] button[type="submit"]').click()
        self.assertIn('Client', self.selenium.find_element_by_css_selector(
            'client:first-of-type').text)

        # If Projects are not viewable, the client name will be in a <span>
        # instead of an <a>.
        self.assertIsInstance(self.selenium.find_element_by_css_selector(
            'client span.text-primary'), FirefoxWebElement)
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_project'))
        self.selenium.refresh()
        self.selenium.find_element_by_css_selector('client a.text-primary')

        # The <client> tag only has two elements when there is no Project add
        # form.
        self.assertEqual(len(self.selenium.find_elements_by_css_selector(
            'client > *')), 2)
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_project'))
        self.selenium.refresh()
        self.selenium.find_element_by_css_selector(
            'client i.fa-chevron-circle-down').click()
        self.selenium.find_element_by_name('project-name').send_keys('Project')
        self.selenium.find_element_by_css_selector(
            'form[name="project-add"] button[type="submit"]').click()
        self.assertIn('Project', self.selenium.find_element_by_css_selector(
            'client project').text)

    def test_entries(self):
        self.logIn()

        self.assertNotIn('Entries', self.selenium.find_element_by_css_selector(
            '#navbarNav').text)
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_entry'))
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_css_selector('a[href="/entries/"]')
        self.selenium.find_element_by_css_selector(
            'a[href="/entries/"]').click()
        self.selenium.find_element_by_id('view-entries')

    def test_reports(self):
        self.logIn()

        self.selenium.find_element_by_css_selector('a[href="/reports/"]')
        self.selenium.find_element_by_css_selector(
            'a[href="/reports/"]').click()
        self.selenium.find_element_by_id('view-reports')
