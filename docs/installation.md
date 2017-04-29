# Installation

For all systems you are going to need:

- Python 2.7, 3.4, 3.5, or 3.6
- Python virtualenv and pip packages
- The ability to compile Python native extensions

Once you have all of that you can run the following and move onto Testing
and/or Running Timestrap:

    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements/development.txt

### Ubuntu

You can install everything you need from apt.

    sudo apt install build-essential python-dev virtualenv python-pip

## Running Timestrap

Always make sure you are in the virtual environment before running additional
commands by first running `source .venv/bin/activate`. If you have already done
this from the previous step and have not left the environment continue on!

If you have not yet migrated your database do so by running:

    python manage.py migrate

You'll need to create your first user too:

    python manage.py createsuperuser

After this you can run Timestrap and access it from your browser at
`localhost:8000`.

    python manage.py runserver

## Generate Fake Data

Want to see how Timestrap would look after being used a while? Run `fake` to
generate some data. Don't run this on a production database or you'll have to
do a lot of clean up.

    python manage.py fake

## Password Resets and Email

To support email for things like password resetting you need to update
Timestrap's settings. I will not presume your email situation and allow you to
do this yourself by reading [Django's documentation](https://docs.djangoproject.com/en/1.11/ref/settings/#email-backend).

If you are using Heroku you can add `sendgrid` to your apps addons on the 
Heroku admin panel or by running:

    heroku addons:create sendgrid

You then need to add these settings to `timestrap/settings/heroku.py`:

    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

## Time and Date Localization

If you wish to change things like the date strings you'll need to play around
with [Django's formtat localization settings](https://docs.djangoproject.com/en/1.11/topics/i18n/formatting/#controlling-localization-in-templates)
in `timestrap/settings/base.py`. We don't do anything to try and localize by
default but we are trying to avoid lock-in to a specific format. If you enable
localization and run into any bugs let us know!
