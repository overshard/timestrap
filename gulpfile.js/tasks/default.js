const gulp = require('gulp');

const spawn = require('child_process').spawn;


gulp.task('default', ['build', 'watch'], function(cb) {
    const command = [ 'run', 'python', 'manage.py', 'runserver' ];
    const args = process.argv;

    if (args[3] == '--public') {
        command.push('0.0.0.0:80');
    }

    spawn(
        'pipenv',
        command,
        {
            stdio: 'inherit'
        }
    ).on('exit', cb);
});
