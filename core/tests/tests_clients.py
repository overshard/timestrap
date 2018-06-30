from decimal import Decimal

from selenium.common.exceptions import NoSuchElementException

from . import SeleniumTestCase

from ..models import Client, Project


class ClientsTestCase(SeleniumTestCase):

    def test_clients_navigation(self):
        nav_clients = self.find('nav-clients')
        nav_clients.click()

        self.find('view-clients')

    def test_clients_visible(self):
        self.test_clients_navigation()

        clients = Client.objects.all()
        for client in clients:
            client_id = 'client-%s' % (client.id,)
            self.find(client_id)

    def test_projects_visible(self):
        self.test_clients_navigation()

        projects = Project.objects.all()
        for project in projects:
            project_id = 'project-%s' % (project.id,)
            self.find(project_id)

    def test_clients_add(self):
        self.test_clients_navigation()

        client_add = self.find('client-add')

        client_add.click()

        client_modal_name = self.find('client-modal-name')
        client_modal_submit = self.find('client-modal-submit')

        client_modal_name.send_keys('new client name')
        client_modal_submit.click()

        view_clients = self.find('view-clients')
        self.contains('new client name', view_clients)

        client = Client.objects.get(name='new client name')
        self.assertEqual(client.name, 'new client name')

    def test_project_add(self):
        self.test_clients_navigation()

        project_add = self.find('project-add')

        project_add.click()

        project_modal_client = self.find('project-modal-client')
        project_modal_name = self.find('project-modal-name')
        project_modal_estimate = self.find('project-modal-estimate')
        project_modal_submit = self.find('project-modal-submit')

        client = Client.objects.first()

        self.select(client.name, project_modal_client)
        project_modal_name.send_keys('new project name')
        project_modal_estimate.send_keys('350')
        project_modal_submit.click()

        view_clients = self.find('view-clients')
        self.contains('new project name', view_clients)
        self.contains('0%', view_clients)

        project = Project.objects.get(name='new project name')
        self.assertEqual(project.name, 'new project name')
        self.assertEqual(project.estimate, Decimal(350))
