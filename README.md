# Timestrap

[![Build Status](https://travis-ci.org/overshard/timestrap.svg?branch=master)](https://travis-ci.org/overshard/timestrap) [![Coverage Status](https://coveralls.io/repos/github/overshard/timestrap/badge.svg?branch=master)](https://coveralls.io/github/overshard/timestrap?branch=master)

Time tracking and invoicing you can host anywhere. Full export support in
multiple formats and easily extensible.


### Warning
This app is currently very unstable as I have just started coding it.
Everything may, and probably will, change.


## Quickstart

Want to get up and running quickly?

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/overshard/timestrap)

We create a default username and password with superuser access to get you
started, please change it via the admin panel:

- Username: `admin`
- Password: `changeme123`


## Demo Website

I've setup an [instance on Heroku](https://timestrap.herokuapp.com/) of
Timestrap that resets every 10 minutes if you want to play with it. The
username and password are set to the same as the Quickstart ones. If someone
messes up the fun for everyone wait till the next reset or start your own
Heroku instance.


## Installation

For all systems you are going to need:

- Python 2.7, 3.4, 3.5, or 3.6
- Python virtualenv and pip packages
- The ability to compile Python native extensions

Once you have all of that you can run the following and move onto Testing
and/or Running Timestrap:

    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

### Ubuntu

You can install everything you need from apt.

    sudo apt install build-essential python-dev virtualenv python-pip

Since we include `psycopg2` for running on Heroku in the `requirements.txt` for
now you will need the build-deps for that or you'll need to remove it from
`requirements.txt` before installing them.

    sudo apt build-dep psycopg2


## Testing

I'm trying to push for 100% code coverage on this project! If you want to add
or change something and test that everything still works you can do so easily
with:

    python manage.py test

If you push code to our primary repository we test for style adherence and code
coverage. If you get a failed build to either of these we won't accept your
code till it's fixed.


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
