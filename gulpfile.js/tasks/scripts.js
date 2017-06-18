const gulp = require('gulp');

const concat = require('gulp-concat');
const tap = require('gulp-tap');
const buffer = require('gulp-buffer');

const vueify = require('vueify');
const browserify = require('browserify');


gulp.task('scripts', ['scripts:vendor', 'scripts:app']);


gulp.task('scripts:vendor', function(){
    return gulp.src([
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/tether/dist/js/tether.min.js',
        'node_modules/bootstrap/dist/js/bootstrap.min.js',
        'node_modules/moment/min/moment.min.js',
        'node_modules/select2/dist/js/select2.min.js',
        'node_modules/pickadate/lib/compressed/picker.js',
        'node_modules/pickadate/lib/compressed/picker.date.js',
        'node_modules/js-cookie/src/js.cookie.js',
        'node_modules/jquery.growl/javascripts/jquery.growl.js'])
        .pipe(concat('bundle-vendor.js'))
        .pipe(gulp.dest('timestrap/static/js/'));
});


gulp.task('scripts:app', function() {
    gulp.src('timestrap/static_src/app.js', { read: false })
        .pipe(tap(function(file) {
            file.contents = browserify(file.path)
                .transform(vueify)
                .bundle()
                .on('error', function(err) {
                    console.log(err.toString());
                    this.emit('end');
                });
        }))
        .pipe(buffer())
        .pipe(concat('bundle-app.js'))
        .pipe(gulp.dest('timestrap/static/js/'));
});
