## Running Timestrap With Gulp

Similar to above you will still need to be in the virtual environment by running
`source .venv/bin/acivate`. Also make sure you've migrated, created a superuser
and the other tasks. Once that is done you can then run Timestrap with Gulp:

    gulp

This provides you with live updated static files for working on the files in
`static_src`. Once you've completed your changes you can stop Gulp, run 
`gulp build` and commit the changes. We do this to reduce the
number of dependencies required to install Timestrap for people who don't want
to update static files source code or dependencies.
