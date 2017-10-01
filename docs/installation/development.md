## Development Installation

**:exclamation: Important Note:** Node is not required for Timestrap to function. Node is 
used for building Timestrap's static files and improving the development 
workflow. This installation procedure is only necessary for making changes to 
static files.

1. Install the requirements:
    - Python 2.7+
    - Node 6+

1. Initiate a virtual environment with the development requirements.

        pip install pipenv && pipenv install --dev

1. Install Node dependencies.

        npm install -g yarn gulp-cli && yarn install --ignore-engines

1. Bootstrap the database and creates the initial site and user
(username: admin, password: admin)

        gulp migrate

1. Run the server!

        gulp

The Timestrap application should now be running at [http://localhost:8000](http://localhost:8000).
Gulp will automatically recognize and recompile changes to any static
files, allowing quick modification and review without starting and stopping
the application.

[Pull requests](https://github.com/overshard/timestrap/pulls) are :+1: welcome 
and :clap: encouraged!
