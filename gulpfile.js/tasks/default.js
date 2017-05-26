var gulp         = require('gulp');

var spawn        = require('child_process').spawn;


gulp.task('default', ['build', 'watch'], function(cb) {
    var runserver = spawn(
        'python',
        [
            'manage.py',
            'runserver'
        ],
        {
            stdio: 'inherit'
        }
    );
    runserver.on('exit', cb);
});
