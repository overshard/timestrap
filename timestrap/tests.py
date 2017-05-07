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
        return self.verifyById('view-dashboard')

    def verifyById(self, id):
        try:
            self.selenium.find_element_by_id(id)
            return True
        except NoSuchElementException:
            return False

    def verifyByXpath(self, xpath):
        try:
            self.selenium.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException:
            return False

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))

        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys(self.profile['username'])
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('incorrect password')
        self.selenium.find_element_by_name('login').click()
        self.assertFalse(self.verifyById('view-dashboard'))

        self.assertTrue(self.logIn())

    def test_clients(self):
        self.logIn()
        self.assertFalse(self.verifyByXpath('//a[@href="/clients/"]'))

        self.user.user_permissions.add(
            Permission.objects.get(codename='view_client'))

        self.selenium.get(self.live_server_url)
        self.assertTrue(self.verifyByXpath('//a[@href="/clients/"]'))

        self.selenium.find_element_by_xpath('//a[@href="/clients/"]').click()
        self.assertTrue(self.verifyById('view-clients'))

    def test_entries(self):
        self.logIn()
        self.assertFalse(self.verifyByXpath('//a[@href="/entries/"]'))

        self.user.user_permissions.add(
            Permission.objects.get(codename='view_entry'))

        self.selenium.get(self.live_server_url)
        self.assertTrue(self.verifyByXpath('//a[@href="/entries/"]'))

        self.selenium.find_element_by_xpath('//a[@href="/entries/"]').click()
        self.assertTrue(self.verifyById('view-entries'))

    def test_reports(self):
        self.logIn()
        self.assertTrue(self.verifyByXpath('//a[@href="/reports/"]'))

        self.selenium.find_element_by_xpath('//a[@href="/reports/"]').click()
        self.assertTrue(self.verifyById('view-reports'))
