var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var riot = require('gulp-riot');
var expect = require('gulp-expect-file');
var spawn = require('child_process').spawn;


gulp.task('styles', function() {
    let files = [
        'node_modules/font-awesome/css/font-awesome.min.css',
        'node_modules/tether/dist/css/tether.min.css',
        'node_modules/bootstrap/dist/css/bootstrap.min.css',
        'node_modules/select2/dist/css/select2.min.css',
        'node_modules/pickadate/lib/compressed/themes/default.css',
        'node_modules/pickadate/lib/compressed/themes/default.date.css',
        'static_src/sass/**/*.scss'
    ]
    gulp.src(files)
        .pipe(expect(files))
        .pipe(sass().on('error', sass.logError))
        .pipe(concat('styles.css'))
        .pipe(gulp.dest('./timestrap/static/css/'));
});


gulp.task('scripts', function(){
    let files = [
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/moment/min/moment.min.js',
        'node_modules/tether/dist/js/tether.min.js',
        'node_modules/bootstrap/dist/js/bootstrap.min.js',
        'node_modules/select2/dist/js/select2.min.js',
        'node_modules/pickadate/lib/compressed/picker.js',
        'node_modules/pickadate/lib/compressed/picker.date.js',
        'node_modules/js-cookie/src/js.cookie.js',
        'node_modules/chart.js/dist/Chart.min.js',
        'node_modules/riot/riot+compiler.min.js',
        'node_modules/riot-route/dist/route.min.js',
        'static_src/scripts/**/*.js'
    ]
    gulp.src(files)
        .pipe(expect(files))
        .pipe(concat('scripts.js'))
        .pipe(gulp.dest('./timestrap/static/js/'));
});


gulp.task('tags', function() {
    let files = [
        'static_src/tags/**/*.tag'
    ]
    gulp.src(files)
        .pipe(expect(files))
        .pipe(riot())
        .pipe(concat('tags.js'))
        .pipe(gulp.dest('./timestrap/static/js/'));
});


gulp.task('extras', function() {
    var files = [
        'node_modules/font-awesome/fonts/*'
    ]
    gulp.src(files)
        .pipe(expect(files))
        .pipe(gulp.dest('./timestrap/static/fonts/'));
});


gulp.task('build', ['styles', 'scripts', 'tags', 'extras']);


gulp.task('watch', function() {
    gulp.watch('static_src/sass/**/*.scss', ['styles']);
    gulp.watch('static_src/scripts/**/*.js', ['styles']);
    gulp.watch('static_src/tags/**/*.tag', ['tags']);
});


gulp.task('default', ['build', 'watch'], function() {
    var runserver = spawn(
        'python',
        ['manage.py', 'runserver'],
        {
            stdio: 'inherit'
        }
    );
});