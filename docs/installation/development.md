## Development Installation

**:exclamation: Important Note:** Node is not required for Timestrap to function. Node is 
used for building Timestrap's static files and improving the development 
workflow. This installation procedure is only necessary for making changes to 
static files.

1. Install the requirements:
    - Python 2.7, 3.4, 3.5, or 3.6
    - Python virtualenv
    - Python pip
    - Node/NPM
    - Gulp
1. Initiate a virtual environment with the development requirements.

        virtualenv .venv
        source .venv/bin/activate
        pip install -r requirements/development.txt
1. Install Node dependencies.

        npm install        
1. Bootstrap the database.

        python manage.py migrate
1. :lock: Create a super user.

        python manage.py createsuperuser
1. Run the server!

        gulp
        
The Timestrap application should now be running at [http://localhost:8000](http://localhost:8000).
Gulp will automatically recognize and recompile changes to any static
files, allowing quick modification and review without starting and stopping
the application. [Pull requests](https://github.com/overshard/timestrap/pulls)
are :+1: welcome and :clap: encouraged!
