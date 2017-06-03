var gulp = require('gulp');

var spawn = require('child_process').spawn;
var spawnSync = require('child_process').spawnSync;


gulp.task('test', function(cb) {
    var test = spawn(
        './manage.py',
        [
            'test'
        ],
        {
            stdio: 'inherit'
        }
    );
    test.on('exit', cb);
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
