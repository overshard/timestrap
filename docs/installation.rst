Installation
============

For all systems you are going to need:
 
- Python 2.7, 3.4, 3.5, or 3.6
- Python virtualenv and pip packages
- The ability to compile Python native extensions
 
Once you have all of that you can run the following and move onto Testing 
and/or Running Timestrap:::
 
   virtualenv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

Ubuntu
######
 
You can install everything you need from apt.::
 
   sudo apt install build-essential python-dev virtualenv python-pip
 
Since we include `psycopg2` for running on Heroku in the `requirements.txt` for 
now you will need the build-deps for that or you'll need to remove it from 
`requirements.txt` before installing them.::
 
   sudo apt build-dep psycopg2