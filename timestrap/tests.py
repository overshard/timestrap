# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
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
        cls.user = fake.simple_profile()
        cls.user['password'] = fake.password()
        User.objects.create_user(cls.user['username'], cls.user['mail'],
                                 cls.user['password'])

        super(SeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def verifyById(self, id):
        try:
            self.selenium.find_element_by_id(id)
            return True
        except NoSuchElementException:
            return False

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))

        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.user['username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('incorrect password')
        self.selenium.find_element_by_name('login').click()
        self.assertFalse(self.verifyById('view-dashboard'))

        username_input = self.selenium.find_element_by_name("username")
        username_input.clear()
        username_input.send_keys(self.user['username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(self.user['password'])
        self.selenium.find_element_by_name('login').click()
        self.assertTrue(self.verifyById('view-dashboard'))
