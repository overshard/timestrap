from random import randint, choice
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from faker import Factory

from timesheets.models import Client, Project, Entry


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
        if not iterations:
            iterations = 5

        for i in range(iterations):
            Client.objects.create(name=fake.company())

        for client in Client.objects.iterator():
            project_iterations = randint(iterations, iterations*2)
            for i in range(project_iterations):
                Project.objects.create(client=client, name=fake.job())

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
        projects = Project.objects.all()

        for project in projects:
            entry_iterations = randint(iterations*2, iterations*4)
            for i in range(entry_iterations):
                date = fake.date_time_between(
                    start_date='-30d',
                    end_date='now',
                    tzinfo=None
                )
                duration = timedelta(
                    hours=randint(0, 3),
                    minutes=randint(1, 60)
                )
                Entry.objects.create(
                    project=project,
                    user=choice(users),
                    date=date,
                    duration=duration,
                    note=fake.sentence(nb_words=6, variable_nb_words=True)
                )

        if verbosity > 0:
            self.stdout.write(
                self.style.SUCCESS('Successfully added fake data.')
            )
