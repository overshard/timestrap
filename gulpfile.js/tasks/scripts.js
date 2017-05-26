var gulp         = require('gulp');

var concat       = require('gulp-concat');
var riot         = require('gulp-riot');


gulp.task('scripts', function(){
    var files = [
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/moment/min/moment.min.js',
        'node_modules/tether/dist/js/tether.min.js',
        'node_modules/bootstrap/dist/js/bootstrap.min.js',
        'node_modules/select2/dist/js/select2.min.js',
        'node_modules/pickadate/lib/compressed/picker.js',
        'node_modules/pickadate/lib/compressed/picker.date.js',
        'node_modules/js-cookie/src/js.cookie.js',
        'node_modules/riot/riot.min.js',
        'node_modules/riot-route/dist/route.min.js',
        'timestrap/static_src/scripts/**/*.js'
    ];
    gulp.src(files)
        .pipe(concat('bundle.js'))
        .pipe(gulp.dest('timestrap/static/js/'));
});


gulp.task('tags', function() {
    var files = [
        'timestrap/static_src/tags/**/*.tag'
    ];
    gulp.src(files)
        .pipe(riot())
        .pipe(concat('bundle-tags.js'))
        .pipe(gulp.dest('timestrap/static/js/'));
});
