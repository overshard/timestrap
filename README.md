Timestrap
=========

Time tracking and invoicing you can host anywhere. Full export support in
multiple formats and easily extensible.


Installation
------------

Your system needs to have Python with virtualenv and pip installed.

    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt


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
