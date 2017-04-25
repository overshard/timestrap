Timestrap
=========

[![Build Status](https://travis-ci.org/overshard/timestrap.svg?branch=master)](https://travis-ci.org/overshard/timestrap) [![Coverage Status](https://coveralls.io/repos/github/overshard/timestrap/badge.svg?branch=master)](https://coveralls.io/github/overshard/timestrap?branch=master)

Time tracking and invoicing you can host anywhere. Full export support in
multiple formats and easily extensible.

**WARNING**: This app is currently very unstable as I have just started coding
it. Everything may, and probably will, change.


Quickstart
----------

Want to get up and running quickly?

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/overshard/timestrap)

We create a default username and password with superuser access to get you
started, please change it via the admin panel:

 + Username: `admin`
 + Password: `changeme123`


Example Website
---------------

I've setup an [instance on Heroku](https://timestrap.herokuapp.com/) of
Timestrap that resets every 10 minutes if you want to play with it. The
username and password are set to the same as the Quickstart ones. If someone
messes up the fun for everyone wait till the next reset or set the project up
yourself.


Installation
------------

Your system needs to have Python with virtualenv and pip installed. If you are
using Ubuntu you also need to install `build-essential` and on Mac `Xcode`. If
you do not want to use postgres or have a problem building because of
`psycopg2` remove that from your `requirements.txt` before `pip install`. In
some cases you may also need to install `python-dev` on Ubuntu.

    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt


Testing
-------

I'm trying to push for 100% code coverage on this project! If you want to add
or change something and test that everything still works you can do so easily
with:

    python manage.py test

If you push code to our primary repository we test for style adherance and code
coverage. If you get a failed build to either of these we won't accept your
code till it's fixed.


Running Timestrap
-----------------

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


Generate Fake Data
------------------

Want to see how Timestrap would look after being used a while? Run `fake` to
generate some data. Don't run this on a production database or you'll have to
do a lot of clean up.

    python manage.py fake


Screenshots
-----------

![Entries](https://raw.githubusercontent.com/overshard/timestrap/master/screenshots/entries.png)
![Dashboard](https://raw.githubusercontent.com/overshard/timestrap/master/screenshots/dashboard.png)
