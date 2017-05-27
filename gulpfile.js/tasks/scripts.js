var gulp = require('gulp');

var concat = require('gulp-concat');
var tap = require('gulp-tap');
var buffer = require('gulp-buffer');

var vueify = require('vueify');
var browserify = require('browserify');


gulp.task('scripts', function(){
    var files = [
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/tether/dist/js/tether.min.js',
        'node_modules/bootstrap/dist/js/bootstrap.min.js',
        'node_modules/moment/min/moment.min.js',
        'node_modules/select2/dist/js/select2.min.js',
        'node_modules/pickadate/lib/compressed/picker.js',
        'node_modules/pickadate/lib/compressed/picker.date.js',
        'node_modules/js-cookie/src/js.cookie.js',
        'timestrap/static_src/scripts/**/*.js'
    ];
    return gulp.src(files)
        .pipe(concat('bundle.js'))
        .pipe(gulp.dest('timestrap/static/js/'));
});


gulp.task('tags', function() {
    var files = [
        'timestrap/static_src/tags/main.js'
    ];
    return gulp.src(files, {read: false})
        .pipe(tap(function(file) {
            file.contents = browserify(file.path, {debug: true})
                .transform(vueify)
                .bundle();
        }))
        .pipe(buffer())
        .pipe(concat('bundle-tags.js'))
        .pipe(gulp.dest('timestrap/static/js/'));
});
