from random import randint, choice
from datetime import datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from faker import Factory

from core.models import Client, Entry, Project, Task


class Command(BaseCommand):
    help = 'Generates a bunch of fake clients, projects, and entries'

    def add_arguments(self, parser):
        parser.add_argument(
            '--iterations',
            dest='iterations',
            default=5,
            help='The amount of data we add do the database'
        )

    def handle(self, *args, **kwargs):
        fake = Factory.create()
        verbosity = kwargs['verbosity']
        iterations = kwargs['iterations']

        for _ in range(iterations):
            task_name = (fake
                         .sentence(nb_words=3, variable_nb_words=True)
                         .replace('.', '')
                         .title())
            Task.objects.create(
                name=task_name,
                hourly_rate=Decimal(
                    '%d.%d' % (randint(1, 200), randint(1, 99)))
            )

        for _ in range(iterations):
            Client.objects.create(name=fake.company())

        for client in Client.objects.iterator():
            for i in range(randint(1, iterations)):
                estimated = choice([True, False])
                estimate = None
                if estimated:
                    estimate = randint(1000, 20000)
                project_name = (fake
                                .sentence(nb_words=3, variable_nb_words=True)
                                .replace('.', '')
                                .title())
                Project.objects.create(
                    client=client,
                    estimate=estimate,
                    name=project_name
                )

        for _ in range(iterations):
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
        projects = Project.objects.all()
        tasks = Task.objects.all()

        for user in users:
            for day in range(iterations):
                date = (datetime.now() - timedelta(days=day)).date()
                for _ in range(randint(1, iterations)):
                    duration = timedelta(minutes=randint(1, 180))
                    Entry.objects.create(
                        project=choice(projects),
                        task=choice(tasks),
                        user=user,
                        date=date,
                        duration=duration,
                        note=fake.sentence(nb_words=6, variable_nb_words=True)
                    )

        if verbosity > 0:
            self.stdout.write(
                self.style.SUCCESS('Successfully added fake data.')
            )
