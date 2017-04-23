Timestrap
=========

[![Travis][travis-shield]][travis-link] [![Coveralls][coveralls-shield]][coveralls-link]  [![License][license-shield]][license-link]

Time tracking and invoicing you can host anywhere. Full export support in
multiple formats and easily extensible.


Quickstart
----------

Want to get up and running quickly?

[![Heroku][heroku-shield]][heroku-link]


Installation
------------

Your system needs to have Python with virtualenv and pip installed.

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

After this you can run Timestrap and access it from your browser at
`localhost:8000`.

    python manage.py runserver


Generate Fake Data
------------------

Want to see how Timestrap would look after being used a while? Run `fake` to
generate some data. Don't run this on a production database or you'll have to
do a lot of clean up.

    python manage.py fake


[travis-shield]: https://img.shields.io/travis/overshard/timestrap.svg?style=flat-square
[travis-link]: https://travis-ci.org/overshard/timestrap
[coveralls-shield]: https://img.shields.io/coveralls/overshard/timetrap.svg?style=flat-square
[coveralls-link]: https://coveralls.io/github/overshard/timestrap
[license-shield]: https://img.shields.io/github/license/overshard/timestrap.svg?style=flat-square
[license-link]: https://github.com/overshard/timestrap/blob/master/LICENSE.md
[heroku-shield]: https://www.herokucdn.com/deploy/button.svg
[heroku-link]: https://heroku.com/deploy?template=https://github.com/overshard/timestrap
