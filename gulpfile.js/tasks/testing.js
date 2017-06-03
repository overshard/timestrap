var gulp         = require('gulp');

var spawn        = require('child_process').spawn;


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
