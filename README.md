# Timestrap

[![Codeship](https://img.shields.io/codeship/2b4e68f0-6085-0136-b7b6-12ab0b7c9909.svg?style=flat-square)](https://app.codeship.com/projects/296301) [![Coveralls](https://img.shields.io/coveralls/overshard/timestrap.svg?style=flat-square)](https://coveralls.io/github/overshard/timestrap) [![license](https://img.shields.io/github/license/overshard/timestrap.svg?style=flat-square)](https://github.com/overshard/timestrap/blob/master/LICENSE.md) [![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg?style=flat-square)](https://gitter.im/overshard/timestrap)

Time tracking you can host anywhere. Full export support in
multiple formats and easily extensible.

![Timestrap](screenshot.png)


## Warning

This app is currently very unstable. Everything may, and probably will, change.
All migrations are going to be wiped and setup properly before release 1.0 so
you will not be able to upgrade to 1.0 from early development.


## Demo

There is a [demo instance of Timestrap](https://timestrap.herokuapp.com/) on
Heroku that resets every 10 minutes.


## Superuser Credentials

All installations and the demo create a superuser to get you started, if this
is a production deployment you will want to change these.

- Username: `admin`
- Password: `admin`


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
    sudo docker-compose down
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
of them by running `gulp --tasks` and I will breifly cover some of them here.

- **gulp** Will run a webserver with django and build the client with webpack
- **gulp lint** Will check all code for style consistency
- **gulp manage:makemigrations** Will generate new migrations if models changes
- **gulp manage:migrate** Makes sure there is a superuser, runs migrations
- **gulp manage:fake** Adds a bunch of fake data for testing
- **gulp manage:reset** Resets the database and adds fake data with a superuser
- **gulp coverage:development** Lints, runs tests, shows coverage report


## User Permissions

You can edit and add new users on the admin panel at `/admin/auth/user/`. You
will need to give new users permissions based on the access you wish them to
have. If you wish someone be able to see all clients and projects to be able to
add them to an entry, but not edit or delete them, you need to give them view
permissions under User permissions. These would be
`core | project | Can view project` and `core | client | Can view client`.


## Configuration

### Security

By default we don't enable TLS/SSL features since this project is often run on
an intranet, locally, or in testing environments. If security is a concern of
yours, and it should be, you will need to enable TLS/SSL on your reverse proxy
and setup a certificate there. On Heroku you can run `heoku certs:auto:enable`
to get a free LetsEncrypt certificate.

You will need to configure two settings when you use TLS/SSL on this project.
The first is to force TLS/SSL when people visit your site and the second is to
make sure that Django REST framework returns corrected URLs behind a reverse
proxy. These can be added to `timestrap/settings/base.py` anywhere:

    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

### Email

Email configuration options are available from the Timestrap admin on a
per-site basis. These settings must be supplied to support features such as
password reset. To access the settings, navigate to `/admin/sites/site/` and
select the site to modify.

If you are using Heroku you can add `sendgrid` to your apps addons on the
Heroku admin panel or by running:

    heroku addons:create sendgrid

### Time and Date Localization

Language and timezone settings are available on a per-site basis in the site
configuration area (`/admin/sites/site/`). Timestrap uses [Moment.js](http://momentjs.com/)
on the frontend so localization will be applied to all dates based on these
settings. We'd like to eventually have localization of everything.

## Sites

Timestrap takes advantage of [Django's "sites" framework](https://docs.djangoproject.com/en/1.11/ref/contrib/sites/)
to support running multiple Timestrap "sites" from a single instance of the
application. This an optional enhancement, and the base Timestrap application
will work fine as a single site without any advanced configuration.

### Single Site

Out of the box, Timestrap is a single site using the fake domain `time.strap`
and name `Timestrap`. Both the name and the domain name are configurable on
the admin.

Any domain will fall back to the default site, but it is recommended to at
least set the site domain setting be updated to match the actual site domain
since emails will use this domain when sending.

### Multiple Sites

Timestrap supports setting up multiple sites with configurations options
available on a per-site basis. This functionality may be useful if, for
example, there is a need to separate departments or functional teams within a
larger group of organization.

Sites can be managed by any user with admin access and appropriate permissions:
either `superuser` or the various `site` and `conf` permissions. Sites are
based on domain and use two primary settings, `domain` and `name` in addition
to the various configuration options available.

#### Data Sharing

All Timestrap data will be related to either one or multiple sites.

- **Clients** and **Tasks** can be related to *multiple* sites.
- **Entries** can be related to a *single* site.

Data with a single-site relationship will automatically be related to the site
it was entered on. This settings can be changed from the admin site.

Currently, multiple site relationships can only be controlled from the admin
site. To use a Client or Task on multiple sites, it must be added to one
site and then modified in the admin site to be related to additional sites.

#### Example: Big Project Builders, Inc.

Big Project Builders, Inc. (BPB) uses Timestrap to keep track of its progress
for various projects & clients. However, with many different teams a single
Timestrap instance would have *a lot* of data and it may come difficulty for
individual employees to keep track of progress. So BPB decides to break the
instance in to multiple sites -

- **timestrap.bpb.io** is the primary instance site, where admin superusers add
the Clients and Projects that BPB is working on.
- **design.timestrap.bpb.io** is used by BPB's designers to assign and track
graphics and design work for projects.
- **development.timestrap.bpb.io** is used by BPB's developers to assign and
track project development.
- **testing.timestrap.bpb.io** is used bu BPB's testing team to record time
spent executing and reporting on project tests.
