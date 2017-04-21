from random import randint, choice
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from faker import Factory

from core.models import Timesheet, Task, Entry


class Command(BaseCommand):
    help = 'Generates a bunch of fake timesheets, tasks, and entries'

    def handle(self, *args, **kwargs):
        fake = Factory.create()
        iterations = 5

        for i in range(iterations):
            Timesheet.objects.create(name=fake.company())

        for timesheet in Timesheet.objects.iterator():
            task_iterations = randint(iterations, iterations*2)
            for i in range(task_iterations):
                Task.objects.create(timesheet=timesheet, name=fake.job())

        for i in range(iterations):
            fake_user = fake.simple_profile(sex=None)
            username = fake_user['username']
            email = fake_user['mail']
            password = fake.password(
                length=10,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True
            )
            User.objects.create_user(username, email, password)

        users = User.objects.all()
        tasks = Task.objects.all()

        for task in tasks:
            entry_iterations = randint(iterations*2, iterations*4)
            for i in range(entry_iterations):
                date = fake.date_time_between(
                    start_date='-30d',
                    end_date='now',
                    tzinfo=None
                )
                duration = timedelta(
                    hours=randint(0, 15),
                    minutes=randint(1, 60)
                )
                Entry.objects.create(
                    task=task,
                    user=choice(users),
                    date=date,
                    duration=duration,
                    note=fake.sentence(nb_words=6, variable_nb_words=True)
                )

        self.stdout.write(self.style.SUCCESS('Successfully added fake data.'))
