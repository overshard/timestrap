# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from faker import Factory


fake = Factory.create()


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
)
class SeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile = fake.simple_profile()
        cls.profile['password'] = fake.password()
        super(SeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

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
        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_id('view-dashboard')

        self.logIn()

    def test_clients(self):
        self.logIn()

        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_css_selector('a[href="/clients/"]')
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_client'))
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_css_selector('a[href="/clients/"]')
        self.selenium.find_element_by_css_selector('a[href="/clients/"]').click()
        self.selenium.find_element_by_id('view-clients')

        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_name('client-add')
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_client'))
        self.selenium.refresh()
        self.selenium.find_element_by_name('client-name').send_keys('Client')
        self.selenium.find_element_by_css_selector(
            'form[name="client-add"] button[type="submit"]').click()
        self.assertIn('Client', self.selenium.find_element_by_css_selector(
            'client:first-of-type').text)

        with self.assertRaises(NoSuchElementException):
            # Chevron to display projects
            self.selenium.find_element_by_css_selector(
                'client i.fa-chevron-circle-down')
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_project'))
        self.selenium.refresh()
        self.selenium.find_element_by_css_selector('client i')

        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_css_selector('project-add')
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_project'))
        self.selenium.refresh()
        self.selenium.find_element_by_css_selector(
            'client i.fa-chevron-circle-down').click()
        self.selenium.find_element_by_name('project-name').send_keys('Project')
        self.selenium.find_element_by_css_selector(
            'form[name="project-add"] button[type="submit"]').click()
        self.assertIn('Project', self.selenium.find_element_by_css_selector(
            'client:first-of-type').text)

    def test_entries(self):
        self.logIn()
        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_css_selector('a[href="/entries/"]')

        self.user.user_permissions.add(
            Permission.objects.get(codename='view_entry'))

        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_css_selector('a[href="/entries/"]')

        self.selenium.find_element_by_css_selector('a[href="/entries/"]').click()
        self.selenium.find_element_by_id('view-entries')

    def test_reports(self):
        self.logIn()
        self.selenium.find_element_by_css_selector('a[href="/reports/"]')

        self.selenium.find_element_by_css_selector('a[href="/reports/"]').click()
        self.selenium.find_element_by_id('view-reports')
