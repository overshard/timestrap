const gulp = require('gulp');

const spawn = require('child_process').spawn;


gulp.task('makemigrations', function(cb) {
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


gulp.task('migrate', function(cb) {
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


gulp.task('createsuperuser', function(cb) {
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


gulp.task('reset', ['reset:flush', 'reset:heroku', 'reset:fake']);


gulp.task('reset:flush', function(cb) {
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


gulp.task('reset:heroku', ['reset:flush'], function(cb) {
    spawn(
        'pipenv',
        [
            'run',
            'python',
            'manage.py',
            'heroku'
        ],
        {
            stdio: 'inherit'
        }
    ).on('exit', cb);
});


gulp.task('reset:fake', ['reset:heroku'], function(cb) {
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
