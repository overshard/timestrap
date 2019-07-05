from decimal import Decimal

from selenium.common.exceptions import NoSuchElementException

from core.models import Client, Project

from . import SeleniumTestCase


class ClientsTestCase(SeleniumTestCase):
    def test_clients_navigation(self):
        nav_clients = self.find("nav-clients")
        nav_clients.click()

        self.find("view-clients")

    def test_clients_visible(self):
        self.test_clients_navigation()

        clients = Client.objects.all()
        for client in clients:
            client_id = "client-%s" % (client.id,)
            self.find(client_id)

    def test_projects_visible(self):
        self.test_clients_navigation()

        projects = Project.objects.all()
        for project in projects:
            project_id = "project-%s" % (project.id,)
            self.find(project_id)

    def test_clients_add(self):
        self.test_clients_navigation()

        client_add = self.find("client-add")

        client_add.click()

        client_modal_name = self.find("client-modal-name")
        client_modal_submit = self.find("client-modal-submit")

        client_modal_name.send_keys("new client name")
        client_modal_submit.click()

        view_clients = self.find("view-clients")
        self.contains("new client name", view_clients)

        client = Client.objects.get(name="new client name")
        self.assertEqual(client.name, "new client name")

    def test_projects_add(self):
        self.test_clients_navigation()

        project_add = self.find("project-add")

        project_add.click()

        project_modal_client = self.find("project-modal-client")
        project_modal_name = self.find("project-modal-name")
        project_modal_estimate = self.find("project-modal-estimate")
        project_modal_submit = self.find("project-modal-submit")

        client = Client.objects.first()

        self.select(client.name, project_modal_client)
        project_modal_name.send_keys("new project name")
        project_modal_estimate.send_keys("350")
        project_modal_submit.click()

        view_clients = self.find("view-clients")
        self.contains("new project name", view_clients)
        self.contains("0%", view_clients)

        project = Project.objects.get(name="new project name")
        self.assertEqual(project.name, "new project name")
        self.assertEqual(project.estimate, Decimal(350))

    def test_clients_delete(self):
        self.test_clients_navigation()

        client = Client.objects.first()
        client_id = "client-%s" % (client.id,)
        client_element = self.find(client_id)
        client_menu = self.find("client-menu", client_element)
        client_menu_delete = self.find("client-menu-delete", client_element)

        client_menu.click()
        client_menu_delete.click()

        self.assertRaises(NoSuchElementException, self.find, client_id)
        self.assertRaises(
            Client.DoesNotExist, Client.objects.get, id=client.id
        )  # noqa: E501

    def test_projects_delete(self):
        self.test_clients_navigation()

        project = Project.objects.first()
        project_id = "project-%s" % (project.id,)
        project_element = self.find(project_id)
        project_menu = self.find("project-menu", project_element)
        project_menu_delete = self.find("project-menu-delete", project_element)

        project_menu.click()
        project_menu_delete.click()

        self.assertRaises(NoSuchElementException, self.find, project_id)
        self.assertRaises(
            Project.DoesNotExist, Project.objects.get, id=project.id
        )  # noqa: E501

    def test_clients_archive(self):
        self.test_clients_navigation()

        client = Client.objects.first()
        client_id = "client-%s" % (client.id,)
        client_element = self.find(client_id)
        client_menu = self.find("client-menu", client_element)
        client_menu_archive = self.find("client-menu-archive", client_element)

        client_menu.click()
        client_menu_archive.click()

        self.assertRaises(NoSuchElementException, self.find, client_id)
        self.assertEqual(Client.objects.get(id=client.id).archive, True)

    def test_projects_archive(self):
        self.test_clients_navigation()

        project = Project.objects.first()
        project_id = "project-%s" % (project.id,)
        project_element = self.find(project_id)
        project_menu = self.find("project-menu", project_element)
        project_menu_archive = self.find(
            "project-menu-archive", project_element
        )  # noqa: E501

        project_menu.click()
        project_menu_archive.click()

        self.assertRaises(NoSuchElementException, self.find, project_id)
        self.assertEqual(Project.objects.get(id=project.id).archive, True)

    def test_clients_change(self):
        self.test_clients_navigation()

        client = Client.objects.first()
        client_id = "client-%s" % (client.id,)
        client_element = self.find(client_id)
        client_menu = self.find("client-menu", client_element)
        client_menu_change = self.find("client-menu-change", client_element)

        client_menu.click()
        client_menu_change.click()

        client_modal_name = self.find("client-modal-name")
        client_modal_submit = self.find("client-modal-submit")

        self.assertEqual(client.name, client_modal_name.get_attribute("value"))

        self.clear(client_modal_name)
        client_modal_name.send_keys("new client name")
        client_modal_submit.click()

        self.contains("new client name", client_element)

        client = Client.objects.get(id=client.id)
        self.assertEqual(client.name, "new client name")

    def test_projects_change(self):
        # TODO: Test changing the projects client
        self.test_clients_navigation()

        project = Project.objects.first()
        project_id = "project-%s" % (project.id,)
        project_element = self.find(project_id)
        project_menu = self.find("project-menu", project_element)
        project_menu_change = self.find("project-menu-change", project_element)

        project_menu.click()
        project_menu_change.click()

        project_modal_name = self.find("project-modal-name")
        project_modal_estimate = self.find("project-modal-estimate")
        project_modal_submit = self.find("project-modal-submit")

        self.assertEqual(
            project.name, project_modal_name.get_attribute("value")
        )  # noqa: E501
        self.assertEqual(
            project.estimate or Decimal(0),
            Decimal(project_modal_estimate.get_attribute("value") or 0),
        )  # noqa: E501

        self.clear(project_modal_name)
        project_modal_name.send_keys("new project name")
        self.clear(project_modal_estimate)
        project_modal_estimate.send_keys("350")
        project_modal_submit.click()

        self.contains("new project name", project_element)
        # Can't check if the page contains the new estimate since we don't have
        # that on the front-end, we display a percent. Work around?

        project = Project.objects.get(id=project.id)
        self.assertEqual(project.name, "new project name")
        self.assertEqual(project.estimate, Decimal(350))
