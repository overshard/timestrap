from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Runs migrations for Heroku'

    def handle(self, *args, **kwargs):
        verbosity = kwargs['verbosity']

        call_command('migrate', verbosity=0)

        if verbosity > 0:
            self.stdout.write(
                self.style.SUCCESS('Successfully ran all Heroku commands.')
            )
