from . import SeleniumTestCase


class LoginTestCase(SeleniumTestCase):

    def test_logout_success(self):
        self.logIn()

        self.driver.get('%s%s' % (self.live_server_url, '/logout/'))

        self.find('registration')

    def test_login_error(self):
        self.driver.get('%s%s' % (self.live_server_url, '/login/'))

        input_username = self.find('input-username')
        input_password = self.find('input-password')
        button_submit = self.find('button-submit')

        input_username.send_keys('admin')
        input_password.send_keys('wrong')
        button_submit.click()

        self.find('registration')
