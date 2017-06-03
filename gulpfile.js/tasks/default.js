const gulp = require('gulp');

const spawn = require('child_process').spawn;


gulp.task('default', ['build', 'watch'], function(cb) {
    spawn(
        'pipenv',
        [
            'run',
            'python',
            'manage.py',
            'runserver'
        ],
        {
            stdio: 'inherit'
        }
    ).on('exit', cb);
});
