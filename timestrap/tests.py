# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.webelement import FirefoxWebElement

from pyvirtualdisplay import Display

from faker import Factory

from timesheets.models import Client, Project


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

        # The client edit button should be disabled for unprivileged users.
        self.assertIsInstance(self.selenium.find_element_by_css_selector(
            'client button:disabled'), FirefoxWebElement)
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_client'))
        self.selenium.refresh()
        self.selenium.find_element_by_css_selector(
            'client button').click()
        self.selenium.find_element_by_css_selector('client input').send_keys(
            'Client Changed')
        self.selenium.find_element_by_css_selector('client button').click()
        self.assertIn(
            'Client Changed',
            self.selenium.find_element_by_css_selector(
                'client:first-of-type').text
        )

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

        # The project edit button should be disabled for unprivileged users.
        self.assertIsInstance(self.selenium.find_element_by_css_selector(
            'project button:disabled'), FirefoxWebElement)
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_project'))
        self.selenium.refresh()
        self.selenium.find_element_by_css_selector(
            'client i.fa-chevron-circle-down').click()
        self.selenium.find_element_by_css_selector(
            'project button').click()
        self.selenium.find_element_by_css_selector('project input').send_keys(
            'Project Changed')
        self.selenium.find_element_by_css_selector('project button').click()
        self.assertIn(
            'Project Changed',
            self.selenium.find_element_by_css_selector(
                'project:first-of-type').text)

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

        client = Client(name="Client", archive=False)
        client.save()
        project = Project(name="Project 1", client=client, archive=False)
        project.save()
        project = Project(name="Project 2", client=client, archive=False)
        project.save()

        # The <entries> tag only has three elements when there is no add form.
        self.assertEqual(len(self.selenium.find_elements_by_css_selector(
            'entries > *')), 3)
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_entry'),
            Permission.objects.get(codename='view_client'),
            Permission.objects.get(codename='view_project'))
        self.selenium.refresh()
        self.selenium.find_element_by_class_name(
            'select2-selection__arrow').click()
        self.selenium.find_element_by_class_name(
            'select2-search__field').send_keys('Project 2')
        self.selenium.find_element_by_class_name(
            'select2-search__field').send_keys(Keys.RETURN)
        self.selenium.find_element_by_css_selector(
            'entries form input[placeholder="Note"').send_keys('Note')
        self.selenium.find_element_by_css_selector(
            'entries form input[placeholder="0:00"').send_keys('0:35')
        self.selenium.find_element_by_css_selector(
            'entries form button').submit()
        self.assertIn('Client\nProject 2\nNote\n0:35',
                      self.selenium.find_element_by_css_selector('entry').text)

        # The <entry> tag does not have an Edit button.
        self.assertNotIn('Edit', self.selenium.find_element_by_css_selector(
            'entry').text)
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_entry'))
        self.selenium.refresh()
        self.selenium.find_element_by_id('entry-edit-menu').click()
        # The second entry is the "Edit" link option. For some reason there are
        # two <a> elements for each dropdown entry and the real one is the
        # second one.
        self.selenium.find_elements_by_css_selector(
            '.dropdown-menu a:nth-of-type(2)')[1].click()
        self.selenium.find_element_by_css_selector(
            'entry .select2-selection__arrow').click()
        self.selenium.find_element_by_class_name(
            'select2-search__field').send_keys('Project 1')
        self.selenium.find_element_by_class_name(
            'select2-search__field').send_keys(Keys.RETURN)
        self.selenium.find_element_by_css_selector(
            'entry input[value="Note"]').clear()
        self.selenium.find_element_by_css_selector(
            'entry input[value="Note"]').send_keys('Changed note')
        self.selenium.find_element_by_css_selector(
            'entry input[value="0:35"]').clear()
        self.selenium.find_element_by_css_selector(
            'entry input[value="0:35"]').send_keys('1.5')
        self.selenium.find_element_by_css_selector(
            'entry button').click()
        self.selenium.refresh()
        self.assertIn('Client\nProject 1\nChanged note\n1:30',
                      self.selenium.find_element_by_css_selector('entry').text)


    def test_reports(self):
        self.logIn()

        self.selenium.find_element_by_css_selector('a[href="/reports/"]')
        self.selenium.find_element_by_css_selector(
            'a[href="/reports/"]').click()
        self.selenium.find_element_by_id('view-reports')
