var gulp = require('gulp');

var concat = require('gulp-concat');
var tap = require('gulp-tap');
var buffer = require('gulp-buffer');

var pump = require('pump');
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


gulp.task('tags', function(cb) {
    function handleError(err) {
        console.log(err.toString());
        this.emit('end');
    }
    pump([
        gulp.src('timestrap/static_src/tags/app.js', { read: false }),
        tap(function(file) {
            file.contents = browserify(file.path, { debug: true })
                .transform(vueify)
                .bundle()
                .on('error', handleError);
        }),
        buffer(),
        concat('bundle-tags.js'),
        gulp.dest('timestrap/static/js/')
    ], cb);
});
