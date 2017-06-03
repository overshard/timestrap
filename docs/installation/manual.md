## Manual Installation

Follow the steps below to install Timestrap locally or on any server. This 
process installs the minimal requirements to *run* Timestrap. For development
requirements and procedures, see [Development Installation](#development-installation).

1. Install the requirements:
    - Python 2.7+

1. Initiate a virtual environment.

        pip install pipenv && pipenv install

1. Bootstrap the database.

        python manage.py migrate

1. :lock: Create a super user.

        python manage.py createsuperuser

1. Run the server!

        python manage.py runserver

The Timestrap application should now be running at [http://localhost:8000](http://localhost:8000).
If it is not, feel free to [create an issue](https://github.com/overshard/timestrap/issues)
to seek assistance or report a bug! :bug:
