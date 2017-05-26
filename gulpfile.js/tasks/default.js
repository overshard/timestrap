var gulp         = require('gulp');

var spawn        = require('child_process').spawn;


gulp.task('default', ['build', 'watch'], function() {
    spawn(
        'python',
        [
            'manage.py',
            'runserver'
        ],
        {
            stdio: 'inherit'
        }
    );
});
