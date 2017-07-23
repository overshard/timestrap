## Quickstart

Want to get up and running quickly? :rocket:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/overshard/timestrap)

For manual deployments to Heroku without using the deploy button, make sure to
create two settings before pushing using `heroku config:set`:

    heroku config:set DJANGO_SETTINGS_MODULE=timestrap.settings.heroku
    heroku config:set SECRET_KEY=ChangeMeToSomethingRandom

After a successful push, log in with the default credentials (below)
and **change the admin password**

:lock: Heroku deployments use a default username and password with superuser 
access, please change it via the admin panel after initial login:

- Username: `admin`
- Password: `admin`
