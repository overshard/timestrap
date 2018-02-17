# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS
from django.utils.six.moves import input


class Command(BaseCommand):
    help = 'Deletes all data from this instance and recreates the original ' \
           'site and default admin account.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false', dest='interactive', default=True,
            help='Tells the command to NOT prompt the user for input of any '
                 'kind.',
        )
        parser.add_argument(
            '--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS,
            help='Nominates a database to flush. Defaults to the "default" '
                 'database.',
        )
        parser.add_argument(
            '--fake',
            dest='iterations',
            default=5,
            help=(
                'Fill the database with fake data after the reset. Provide a '
                'number a number of iterations to perform (higher number = '
                'more fake data).'
            ),
        )

    def handle(self, *args, **kwargs):
        interactive = kwargs['interactive']
        database = kwargs['database']
        verbosity = kwargs['verbosity']
        iterations = int(kwargs['iterations'])

        if interactive:
            confirm = input("""You have requested a reset of the application.

This will IRREVERSIBLY DESTROY all data currently in the
database, establish the initial site, and create the initial
admin user.

Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: """)
        else:
            confirm = 'yes'

        if confirm == 'yes':
            try:
                call_command('flush', database=database, interactive=False,
                             verbosity=verbosity)
                self.stdout.write(
                    self.style.SUCCESS('Successfully flushed database.')
                )
            except CommandError:
                self.stdout.write(
                    self.style.ERROR('Database flush failed. Reset aborted.')
                )
                return
            call_command('migrate', verbosity=verbosity)

            if iterations > 0:
                call_command('fake', verbosity=verbosity,
                             iterations=iterations)

            if verbosity > 0:
                self.stdout.write(
                    self.style.SUCCESS('Reset operation complete.')
                )
        else:
            if verbosity > 0:
                self.stdout.write(
                    self.style.ERROR('Reset operation cancelled.')
                )
