var gulp         = require('gulp');

var spawn        = require('child_process').spawn;


gulp.task('makemigrations', function(cb) {
    var makemigrations = spawn(
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
    );
    makemigrations.on('exit', cb);
});


gulp.task('migrate', function(cb) {
    var migrate = spawn(
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
    );
    migrate.on('exit', cb);
});


gulp.task('createsuperuser', function(cb) {
    var createsuperuser = spawn(
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
    );
    createsuperuser.on('exit', cb);
});


gulp.task('reset:flush', function(cb) {
    var flush = spawn(
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
    );
    flush.on('exit', cb);
});


gulp.task('reset:heroku', ['reset:flush'], function(cb) {
    var heroku = spawn(
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
    );
    heroku.on('exit', cb);
});


gulp.task('reset:fake', ['reset:heroku'], function(cb) {
    var fake = spawn(
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
    );
    fake.on('exit', cb);
});


gulp.task('reset', ['reset:flush', 'reset:heroku', 'reset:fake']);
