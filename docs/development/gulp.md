## Gulp Command Reference

Although it is entirely optional, Timestrap makes extensive use of custom Gulp
commands to ease the development process. Review the `gulpfile.js` directory
and files within for a complete understanding of available commands. The
reference below outlines the basic function of each command.

### `gulp`

Builds all required assets, runs the Django development server, and watches for
changes to asset/source files, rebuilding and restarting as necessary.

### `gulp build`

Effectively runs:

1. `gulp styles`
1. `gulp scripts`
1. `gulp extras`

### `gulp docs`

Build GitHub and RTD style documentation files and watching source files for
changes, creating updated builds as necessary.

### `gulp extras`

Copies `extrasFiles` from vendor folders to `/timestrap/static/` folders.

### `gulp lint`

Executes Python, SASS and JavaScript ES6 linting on all source files.

### `gulp manage:makemigrations`

A simple alias for Django's `python manage.py makemigrations` command.

### `gulp manage:migrate`

A simple alias for Django's `python manage.py migrate` command.

### `gulp manage:createsuperuser`

A simple alias for Django's `python manage.py createsuperuser` command.

### `gulp manage:reset`

This command effectively runs:

1. `python manage.py flush` to clear all data from the database and re-execute
post-migration hooks.
1. `python manage.py migrate` to establish the initial site and user.
1. `python manage.py fake` to generate fake data in the database.

The argument `--fake 0` can be used to bypass the fake data generation.

### `gulp scripts`

Compiles JavaScript assets from Timestrap's VueJS files in to `bundle-app.js`
and vendor assets in to `bundle-vendor.js`, placing both in the
`/timestrap/static/js/` folder.

### `gulp styles`

Compiles vendor CSS in to `bundle-vendor.css` and Timestrap's SASS in to
`bundle-scss.css`, placing both in the `/timestrap/static/css/` folder.

### `gulp test`

A alias for Django's `python manage.py test` command. If you wish to run a
specific test you can do so with `--test` as in
`--test core.tests.tests_login.LoginTestCase`. You can also disable headless
mode of see what's going on during the tests with `--head`.

### `gulp coverage`

Runs the `python manage.py test` command and prints a test coverage report when
finished.
