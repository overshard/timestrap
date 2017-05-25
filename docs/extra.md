






## Testing

We use selenium with the chromedriver for testing. If you wish to run tests you
will need to make sure you have Chrome installed. For installation instructions
on those see the above documentation

I'm trying to push for 100% code coverage on this project! If you want to add
or change something and test that everything still works you can do so easily
with:

    python manage.py test

If you push code to our primary repository we test for style adherence and code
coverage. If you get a failed build to either of these we won't accept your
code till it's fixed.

### Sauce Labs

In order to run Selenium tests in a consistent environment, this project makes
use of [SauceLabs](https://saucelabs.com/) for browser testing. To run tests on
SauceLabs, you will need to first create an account. Once you have your 
username and access key, follow the steps below:

Install the sc proxy client

    wget https://saucelabs.com/downloads/sc-4.4.6-linux.tar.gz
    tar zxf sc-4.4.6-linux.tar.gz
    mv sc-4.4.6-linux/bin/sc /usr/local/bin

From within the virtual environment

    pip install sauceclient
    export SAUCE_USERNAME=[YOUR USERNAME]
    export SAUCE_ACCESS_KEY=[YOUR ACCESS KEY]
    sc &

After "Sauce Connect is up, you may start your tests."

    python manage.py test

### Running Timestrap With Gulp

Similar to above you will still need to be in the virtual environment by running
`source .venv/bin/acivate`. Also make sure you've migrated, created a superuser
and the other tasks. Once that is done you can then run Timestrap with Gulp:

    gulp

This provides you with live updated static files for working on the files in
`static_src`. Once you've completed your changes you can stop Gulp, run 
`gulp build` and commit the changes. We do this to reduce the
number of dependencies required to install Timestrap for people who don't want
to update static files source code or dependencies.


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
with [Django's format localization settings](https://docs.djangoproject.com/en/1.11/topics/i18n/formatting/#controlling-localization-in-templates)
in `timestrap/settings/base.py`. We don't do anything to try and localize by
default but we are trying to avoid lock-in to a specific format. If you enable
localization and run into any bugs let us know!
