## Docker Installation

Follow the steps below to install Timestrap locally or on any server. This
process installs the minimal requirements to *run* Timestrap. For development
requirements and procedures, see [Development Installation](#development-installation).

1. Install the requirements:
    - Docker
    - Docker Compose

1. Set any custom configuration options you need and run

        docker-compose up -d

1. Bootstrap the database and creates the initial site and user
(username: admin, password: admin)

        docker-compose exec web python3 manage.py migrate --settings=timestrap.settings.docker

The Timestrap application should now be running at [http://localhost/](http://localhost/).
If it is not, feel free to [create an issue](https://github.com/overshard/timestrap/issues)
to seek assistance or report a bug! :bug:
