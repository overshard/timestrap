Welcome to Timestrap's documentation!
=====================================
Time tracking and invoicing you can host anywhere. Full export support in multiple formats and easily extensible.

.. warning::
   This app is currently very unstable as I have just started coding it. Everything may, and probably will, change.

Quickstart
##########
Want to get up and running quickly?

 .. image:: https://www.herokucdn.com/deploy/button.svg
   :target: https://heroku.com/deploy?template=https://github.com/overshard/timestrap
 
We create a default username and password with superuser access to get you started, please change it via the admin panel:
 
 - Username: `admin`
 - Password: `changeme123`
 
If you are manually deploying to Heroku without using the deploy button make
sure you create two settings before pushing using `heroku config:set`:::

   heroku config:set DJANGO_SETTINGS_MODULE=timestrap.settings.heroku
   heroku config:set SECRET_KEY=ChangeMeToSomethingRandom

You will also need to create a superuser after your push has been successful in order to login:::

   heroku run python manage.py createsuperuser

Demo Website
############
I've setup an `instance on Heroku <https://timestrap.herokuapp.com/>`_ of Timestrap that resets every 10 minutes 
if you want to play with it. The username and password are set to the same as the Quickstart ones. If someone messes 
up the fun for everyone wait till  the next reset or start your own Heroku instance.


More Documentation
##################
.. toctree::
   :maxdepth: 2

   installation.rst

