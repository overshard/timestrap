var gulp         = require('gulp');


var spawn        = require('child_process').spawn;
var spawnSync    = require('child_process').spawnSync;


gulp.task('test', function() {
    spawnSync(
        'python',
        [
            'manage.py',
            'test'
        ],
        {
            stdio: 'inherit'
        }
    );
});


gulp.task('coverage', function() {
    spawnSync(
        'coverage',
        [
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
        'coverage',
        [
            'report',
            '-m'
        ],
        {
            stdio: 'inherit'
        }
    );
});
