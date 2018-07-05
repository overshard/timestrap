from time import sleep
from decimal import Decimal

from selenium.common.exceptions import NoSuchElementException

from core.models import Task

from . import SeleniumTestCase


class TasksTestCase(SeleniumTestCase):

    def test_tasks_navigation(self):
        nav_tasks = self.find('nav-tasks')
        nav_tasks.click()

        self.find('view-tasks')

    def test_tasks_visible(self):
        self.test_tasks_navigation()

        tasks = Task.objects.all()
        for task in tasks:
            task_id = 'task-%s' % (task.id,)
            self.find(task_id)

    def test_tasks_add(self):
        self.test_tasks_navigation()

        task_add = self.find('task-add')

        task_add.click()

        task_modal_name = self.find('task-modal-name')
        task_modal_hourly_rate = self.find('task-modal-hourly-rate')
        task_modal_submit = self.find('task-modal-submit')

        task_modal_name.send_keys('new task name')
        task_modal_hourly_rate.send_keys('3.50')
        task_modal_submit.click()

        view_tasks = self.find('view-tasks')
        self.contains('new task name', view_tasks)
        self.contains('3.50', view_tasks)

        task = Task.objects.get(name='new task name')
        self.assertEqual(task.name, 'new task name')
        self.assertEqual(task.hourly_rate, Decimal(3.50))

    def test_tasks_delete(self):
        self.test_tasks_navigation()

        task = Task.objects.first()
        task_id = 'task-%s' % (task.id,)
        task_element = self.find(task_id)
        task_menu = self.find('task-menu', task_element)
        task_menu_delete = self.find('task-menu-delete', task_element)

        task_menu.click()
        task_menu_delete.click()

        sleep(2)

        self.assertRaises(NoSuchElementException, self.find, task_id)
        self.assertRaises(Task.DoesNotExist, Task.objects.get, id=task.id)

    def test_tasks_change(self):
        self.test_tasks_navigation()

        task = Task.objects.first()
        task_id = 'task-%s' % (task.id,)
        task_element = self.find(task_id)
        task_menu = self.find('task-menu', task_element)
        task_menu_change = self.find('task-menu-change', task_element)

        task_menu.click()
        task_menu_change.click()

        task_modal_name = self.find('task-modal-name')
        task_modal_hourly_rate = self.find('task-modal-hourly-rate')
        task_modal_submit = self.find('task-modal-submit')

        self.assertEqual(task.name, task_modal_name.get_attribute('value'))
        self.assertEqual(task.hourly_rate, Decimal(task_modal_hourly_rate.get_attribute('value')))  # noqa: E501

        self.clear(task_modal_name)
        task_modal_name.send_keys('new task name')
        self.clear(task_modal_hourly_rate)
        task_modal_hourly_rate.send_keys('3.50')
        task_modal_submit.click()

        self.contains('new task name', task_element)
        self.contains('3.50', task_element)

        task = Task.objects.get(id=task.id)
        self.assertEqual(task.name, 'new task name')
        self.assertEqual(task.hourly_rate, Decimal(3.50))
