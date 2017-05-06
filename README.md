# Timestrap

[![Travis](https://img.shields.io/travis/overshard/timestrap.svg?style=flat-square)](https://travis-ci.org/overshard/timestrap) [![Coveralls](https://img.shields.io/coveralls/overshard/timestrap.svg?style=flat-square)](https://coveralls.io/github/overshard/timestrap) [![license](https://img.shields.io/github/license/overshard/timestrap.svg?style=flat-square)](https://github.com/overshard/timestrap/blob/master/LICENSE.md)

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

If you are manually deploying to Heroku without using the deploy button make
sure you create two settings before pushing using `heroku config:set`:

    heroku config:set DJANGO_SETTINGS_MODULE=timestrap.settings.heroku
    heroku config:set SECRET_KEY=ChangeMeToSomethingRandom

You will also need to create a superuser after your push has been successful in
order to login:

    heroku run python manage.py createsuperuser

And finally you need to setup multiple buildpacks because we use yarn for our
static files:

    heroku buildpacks:set heroku/python
    heroku buildpacks:add --index 1 heroku/nodejs

## Demo Website

I've setup an [instance on Heroku](https://timestrap.herokuapp.com/) of
Timestrap that resets every 10 minutes if you want to play with it. The
username and password are set to the same as the Quickstart ones. If someone
messes up the fun for everyone wait till the next reset or start your own
Heroku instance.


## Installation

For all systems you are going to need:

- Python
- Python virtualenv and pip packages
- The ability to compile Python native extensions
- Node.js with with npm

Once you have all of that you can run the following and move onto Testing
and/or Running Timestrap:

    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements/development.txt


### Ubuntu

You can install everything you need from apt. A note about node on Ubuntu, it
installs to `/usr/bin/nodejs` and every node project checks `/usr/bin/node` so
we have to create a link between the two.

    sudo apt install build-essential python-dev virtualenv python-pip npm
    sudo npm install -g yarn
    sudo ln -s /usr/bin/nodejs /usr/bin/node


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

We need to fetch our JS and CSS dependencies:

    yarn install --modules-folder timestrap/static/vendor

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
