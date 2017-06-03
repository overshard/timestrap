const gulp = require('gulp');

const spawn = require('child_process').spawn;
const spawnSync = require('child_process').spawnSync;


gulp.task('test', function(cb) {
    spawn(
        './manage.py',
        [
            'test'
        ],
        {
            stdio: 'inherit'
        }
    ).on('exit', cb);
});


gulp.task('coverage', function() {
    spawnSync(
        'pipenv',
        [
            'run',
            'coverage',
            'run',
            '--source=core,api',
            'manage.py',
            'test'
        ],
        {
            stdio: 'inherit'
        }
    );
    spawnSync(
        'pipenv',
        [
            'run',
            'coverage',
            'report',
            '-m'
        ],
        {
            stdio: 'inherit'
        }
    );
});
