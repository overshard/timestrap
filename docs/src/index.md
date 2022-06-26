# Timestrap

[![license](https://img.shields.io/github/license/overshard/timestrap.svg?style=for-the-badge)](https://github.com/overshard/timestrap/blob/master/LICENSE.md)

Time tracking you can host anywhere. Full export support in
multiple formats and easily extensible.


## Warning

This app is currently very unstable. Everything may, and probably will, change.
All migrations are going to be wiped and setup properly before release 1.0 so
you will not be able to upgrade to 1.0 from early development.


## Documentation

For more details and screenshots check out our main docs website:
[https://timestrap.bythewood.me/](https://timestrap.bythewood.me/)


## Superuser Credentials

All installations and the demo create a superuser to get you started, if this
is a production deployment you will want to change these.

- Username: `admin`
- Password: `admin`


## Docker Installation

This creates a minimal docker server setup for Timestrap. This currently is
in development and may not have persistent data without fiddling. Any help to
improve the docker configuration files would be appreciated.

### Docker Requirements

- Docker
- Docker Compose

Docker Compose is used for running multiple containers since we require a
PostgreSQL database and, not yet but soon, a Redis server for messages and
events.

### Docker Running

Make sure to update the environmental variables in `docker-compose.yml` and
check the `timestrap/settings/docker.py` file to see if you'd like to change
anything then run:

    sudo docker-compose up --detach

To migrate the database, create your first superuser, and create the initial
site configuration you then need to run:

    sudo docker-compose exec web python3 manage.py migrate --settings=timestrap.settings.docker

The Timestrap application should now be running on port 80 of whatever system
you ran these commands on, if you ran this locally then that would be
[http://localhost/](http://localhost/).

### Docker Data

All data should be stored in the timestrap_db volume. If you wish to rebuild
Timestrap at the latest you can do the following from the timestrap repo you
cloned:

    git pull
    sudo docker-compose stop
    sudo docker-compose build
    sudo docker-compose up --detach
    sudo docker-compose exec web python3 manage.py migrate --settings=timestrap.settings.docker

All data will be kept during this process and you'll have the latest version
of Timestrap.

## Development Installation

If you'd like to contribute code to Timestrap you'll need to do this!

### Development Requirements

- Python 3.5+
- Python Dev
- Node 8+
- pipenv
- npm
- Firefox
- geckodriver

Python 3.5+ is required because we use async/await with Channels to support
WebSockets and add realtime updates to the client. Python Dev is not required
on macOS but if you are on Linux, like Ubuntu, you will need to install it with
`sudo apt install python3-dev`.

Node 8+ isn't exactly required, you might be able to get away with an older
version and we only use node for building the client.

You'll probably need to install pipenv with pip, run `pip install pipenv` to
get this. It's just a better python package manager that allows us to lock our
dependencies.

Node installs npm by default but you may want to install the latest with
`npm install --global npm`.

Firefox is used for functional/selenium tests in conjunction with geckodriver,
you can get geckodriver from [mozilla's offical releases](https://github.com/mozilla/geckodriver/releases)
or you might be able to install it with your systems package manager. Brew on
macOS has this with `brew install geckodriver`. If you have to download it
manually make sure to extract it in some sort of `bin` directory e.g.
`/usr/local/bin/`.

### Development Setup

Once you have all of the above you can get started! For the global npm install
on gulp-cli you may need to run this with sudo depending on how you installed
everything above.

    npm install --global gulp-cli
    npm install
    pipenv install --dev

After all the dependencies install you can migrate the database and run the
server.

    gulp manage:migrate
    gulp

If you'd like to have some sample data to work with you can run
`gulp manage:fake` after you run `gulp manage:migrate`.

Timestrap should now be running at [http://localhost:8000](http://localhost:8000)
and gulp + django's test server will automatically recognize and recompile
changes to any file allowing for quick modification and review.

Once you've made your changes you can test with `gulp coverage:development` and
if that is successful and you want to share your changes create a
[pull request](https://github.com/overshard/timestrap/pulls)!

### Development Commands

I've prebuilt a variety of build commands for development, you can see a list
of them by running `gulp --tasks` and I will briefly cover some of them here.

- `gulp` Will run a webserver with django and build the client with webpack
- `gulp lint` Will check all code for style consistency
- `gulp manage:makemigrations` Will generate new migrations if models changes
- `gulp manage:migrate` Makes sure there is a superuser, runs migrations
- `gulp manage:fake` Adds a bunch of fake data for testing
- `gulp manage:reset` Resets the database and adds fake data with a superuser
- `gulp coverage:development` Lints, runs tests, shows coverage report
