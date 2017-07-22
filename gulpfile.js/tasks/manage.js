const gulp = require('gulp');

const spawn = require('child_process').spawn;


gulp.task('makemigrations', cb => {
    spawn(
        'pipenv',
        [
            'run',
            'python',
            'manage.py',
            'makemigrations'
        ],
        {
            stdio: 'inherit'
        }
    ).on('exit', cb);
});


gulp.task('migrate', cb => {
    spawn(
        'pipenv',
        [
            'run',
            'python',
            'manage.py',
            'migrate'
        ],
        {
            stdio: 'inherit'
        }
    ).on('exit', cb);
});


gulp.task('createsuperuser', cb => {
    spawn(
        'pipenv',
        [
            'run',
            'python',
            'manage.py',
            'createsuperuser'
        ],
        {
            stdio: 'inherit'
        }
    ).on('exit', cb);
});


gulp.task('reset', ['reset:flush', 'reset:load', 'reset:fake']);


gulp.task('reset:flush', cb => {
    spawn(
        'pipenv',
        [
            'run',
            'python',
            'manage.py',
            'flush',
            '--noinput'
        ],
        {
            stdio: 'inherit'
        }
    ).on('exit', cb);
});


gulp.task('reset:load', ['reset:flush'], cb => {
    spawn(
        'pipenv',
        [
            'run',
            'python',
            'manage.py',
            'loaddata',
            'initial_data.json'
        ],
        {
            stdio: 'inherit'
        }
    ).on('exit', cb);
});


gulp.task('reset:fake', ['reset:load'], cb => {
    spawn(
        'pipenv',
        [
            'run',
            'python',
            'manage.py',
            'fake'
        ],
        {
            stdio: 'inherit'
        }
    ).on('exit', cb);
});
