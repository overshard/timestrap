# Timestrap [![Travis](https://img.shields.io/travis/overshard/timestrap.svg?style=flat-square)](https://travis-ci.org/overshard/timestrap) [![Coveralls](https://img.shields.io/coveralls/overshard/timestrap.svg?style=flat-square)](https://coveralls.io/github/overshard/timestrap) [![license](https://img.shields.io/github/license/overshard/timestrap.svg?style=flat-square)](https://github.com/overshard/timestrap/blob/master/LICENSE.md)

Time tracking and invoicing you can host anywhere. Full export support in
multiple formats and easily extensible.

![Timestrap](screenshot.png)

### :warning: Warning

This app is currently very unstable. Everything may, and probably will, change.

## Demo

There is a [demo instance of Timestrap](https://timestrap.herokuapp.com/) on
Heroku that resets every 10 minutes. The default credentials are:

- Username: `admin`
- Password: `changeme123`

## Quickstart

Want to get up and running quickly? :rocket:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/overshard/timestrap)

The Heroku deployment has a default username and password with superuser 
access, please change it via the admin panel:

- Username: `admin`
- Password: `changeme123`

For manual deployments to Heroku without using the deploy button, make sure to
create two settings before pushing using `heroku config:set`:

    heroku config:set DJANGO_SETTINGS_MODULE=timestrap.settings.heroku
    heroku config:set SECRET_KEY=ChangeMeToSomethingRandom

:lock: After a successful push, create a super user to allow login:

    heroku run python manage.py createsuperuser

## Manual Installation

Follow the steps below to install Timestrap locally or on any server. This 
process installs the minimal requirements to *run* Timestrap. For development
requirements and procedures, see [Development Installation](#development-installation).

1. Install the requirements:
    - Python 2.7, 3.4, 3.5, or 3.6
    - Python virtualenv
    - Python pip
1. Initiate a virtual environment.

        virtualenv .venv
        source .venv/bin/activate
        pip install -r requirements/base.txt
1. Bootstrap the database.

        python manage.py migrate
1. :lock: Create a super user.

        python manage.py createsuperuser
1. Run the server!

        python manage.py runserver
        
The Timestrap application should now be running at [http://localhost:8000](http://localhost:8000).
If it is not, feel free to [create an issue](https://github.com/overshard/timestrap/issues)
to seek assistance or report a bug! :bug:

## Development Installation

**:exclamation: Important Note:** Node is not required for Timestrap to function. Node is 
used for building Timestrap's static files and improving the development 
workflow. This installation procedure is only necessary for making changes to 
static files.

1. Install the requirements:
    - Python 2.7, 3.4, 3.5, or 3.6
    - Python virtualenv
    - Python pip
    - Node/NPM
    - Gulp
1. Initiate a virtual environment with the development requirements.

        virtualenv .venv
        source .venv/bin/activate
        pip install -r requirements/development.txt
1. Install Node dependencies.

        npm install        
1. Bootstrap the database.

        python manage.py migrate
1. :lock: Create a super user.

        python manage.py createsuperuser
1. Run the server!

        gulp
        
The Timestrap application should now be running at [http://localhost:8000](http://localhost:8000).
Gulp will automatically recognize and recompile changes to any static
files, allowing quick modification and review without starting and stopping
the application. [Pull requests](https://github.com/overshard/timestrap/pulls)
are :+1: welcome and :clap: encouraged!

## Further Reading

For additional documentation on [configuration options](RTD), [installing requirements](RTD), 
[testing](RTD) and more, please see [https://timestrap.readthedocs.io/](https://timestrap.readthedocs.io/).
