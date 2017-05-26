var gulp         = require('gulp');

var spawn        = require('child_process').spawn;


gulp.task('makemigrations', function(cb) {
    var makemigrations = spawn(
        './manage.py',
        [
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
        './manage.py',
        [
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
        './manage.py',
        [
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
        './manage.py',
        [
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
        './manage.py',
        [
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
        './manage.py',
        [
            'fake'
        ],
        {
            stdio: 'inherit'
        }
    );
    fake.on('exit', cb);
});


gulp.task('reset', ['reset:flush', 'reset:heroku', 'reset:fake']);
