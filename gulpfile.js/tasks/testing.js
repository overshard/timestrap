const gulp = require('gulp');

const spawn = require('child_process').spawn;
const spawnSync = require('child_process').spawnSync;


gulp.task('test', function(cb) {
    let command = [ 'run', 'python', 'manage.py', 'test' ];
    let args = process.argv;
    if (args[3] == '--test' && args[4]) {
        command.push(args[4]);
    }
    spawn(
        'pipenv',
        command,
        {
            stdio: 'inherit'
        }
    ).on('exit', (code) => {
        process.exit(code);
    });
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
