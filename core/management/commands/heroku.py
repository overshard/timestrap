from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Creates a superuser for Heroku'

    def handle(self, *args, **kwargs):
        verbosity = kwargs['verbosity']

        call_command('migrate', verbosity=0)

        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='changeme123'
        )

        if verbosity > 0:
            self.stdout.write(
                self.style.SUCCESS('Successfully run all Heroku commands.')
            )
