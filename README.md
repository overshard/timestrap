# Timestrap

[![Travis](https://img.shields.io/travis/overshard/timestrap.svg?style=for-the-badge)](https://travis-ci.org/overshard/timestrap) [![Coveralls](https://img.shields.io/coveralls/overshard/timestrap.svg?style=for-the-badge)](https://coveralls.io/github/overshard/timestrap) [![license](https://img.shields.io/github/license/overshard/timestrap.svg?style=for-the-badge)](https://github.com/overshard/timestrap/blob/master/LICENSE.md)

Time tracking you can host anywhere. Full export support in
multiple formats and easily extensible.

## Warning

This app is currently very unstable. Everything may, and probably will, change.
All migrations are going to be wiped and setup properly before release 1.0 so
you will not be able to upgrade to 1.0 from early development.

## Documentation

For more details and screenshots check out our main docs website:
[https://docs.gettimestrap.com/](https://docs.gettimestrap.com/)

## Demo

There is a [demo instance of Timestrap](https://timestrap.herokuapp.com/) on
Heroku that resets every 10 minutes.

## Superuser Credentials

All installations and the demo create a superuser to get you started, if this
is a production deployment you will want to change these.

-   Username: `admin`
-   Password: `admin`

## Heroku Installation

The easiest way to run Timestrap and the only installation that I can actively
support since I use it myself in production.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/overshard/timestrap)

For manual deployments to Heroku, make sure to create two environmental
variables before pushing using `heroku config:set`:

    heroku config:set DJANGO_SETTINGS_MODULE=timestrap.settings.heroku
    heroku config:set SECRET_KEY=ChangeMeToSomethingRandom

## Docker Installation

This creates a minimal docker server setup for Timestrap. This currently is
in development and may not have persistent data without fiddling. Any help to
improve the docker configuration files would be appreciated.

### Docker Requirements

-   Docker
-   Docker Compose

Docker Compose is used for running multiple containers since we require a
PostgreSQL database and, not yet but soon, a Redis server for messages and
events.

### Docker Running

Make sure to update the environmental variables in `docker-compose.yml` and
check the `timestrap/settings/docker.py` file to see if you'd like to change
anything then run:

    docker-compose up --detach --build

To migrate the database, create your first superuser, and create the initial
site configuration you then need to run:

    docker-compose exec web python3 manage.py migrate

The Timestrap application should now be running on port 80 of whatever system
you ran these commands on, if you ran this locally then that would be
[http://localhost/](http://localhost/).

### Docker Data

All data should be stored in the timestrap_db volume. If you wish to rebuild
Timestrap at the latest you can do the following from the timestrap repo you
cloned:

    git pull
    docker-compose up --detach --build
    docker-compose exec web python3 manage.py migrate

All data will be kept during this process and you'll have the latest version
of Timestrap.

## Development Installation

If you'd like to contribute code to Timestrap you'll need to do this!

### Development Requirements

-   Python 3.7+
-   Node 10+
-   pipenv
-   yarn

You'll probably need to install pipenv with pip, run `pip install pipenv` to
get this. Same with yarn for node, `npm install --global yarn`. On some systems
you may have to install some additional development files. For example on
Ubuntu you will need to install `apt install build-essential`. On Alpine you
will need `apk add python3-dev nodejs-dev postgresql-dev gcc musl-dev`;

### Development Setup

Once you have all of the above you can get started!

    yarn install
    pipenv install --dev

After all the dependencies install you can migrate the database and run the
server.

    pipenv run python manage.py migrate
    pipenv run python manage.py fake
    yarn start

Timestrap should now be running at [http://localhost:8000](http://localhost:8000)
and the test server will automatically recognize and recompile changes to any
file allowing for quick modification and review.

Once you've made your changes you can share your changes by creating a
[pull request](https://github.com/overshard/timestrap/pulls)!
