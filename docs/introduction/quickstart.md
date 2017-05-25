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
