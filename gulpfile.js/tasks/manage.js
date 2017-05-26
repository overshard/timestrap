var gulp         = require('gulp');


var spawn        = require('child_process').spawn;
var spawnSync    = require('child_process').spawnSync;


function manageSync(command) {
    var fullCommand = ['manage.py'].concat(command);
    spawnSync(
        'python',
        fullCommand,
        {
            stdio: 'inherit'
        }
    );
}


gulp.task('makemigrations', function() {
    manageSync(['makemigrations']);
});


gulp.task('migrate', function() {
    manageSync(['migrate']);
});


gulp.task('createsuperuser', function() {
    manageSync(['createsuperuser']);
});


gulp.task('reset', function() {
    manageSync(['flush', '--noinput']);
    manageSync(['heroku']);
    manageSync(['fake']);
});
