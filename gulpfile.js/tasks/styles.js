var gulp         = require('gulp');

var concat       = require('gulp-concat');
var sass         = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');


gulp.task('styles:vendor', function() {
    var files = [
        'node_modules/font-awesome/css/font-awesome.min.css',
        'node_modules/tether/dist/css/tether.min.css',
        'node_modules/bootstrap/dist/css/bootstrap.min.css',
        'node_modules/select2/dist/css/select2.min.css',
        'node_modules/pickadate/lib/compressed/themes/default.css',
        'node_modules/pickadate/lib/compressed/themes/default.date.css',
    ];
    gulp.src(files)
        .pipe(concat('bundle-vendor.css'))
        .pipe(gulp.dest('timestrap/static/css/'));
});


gulp.task('styles:scss', function() {
    var files = [
        'timestrap/static_src/sass/**/*.scss'
    ];
    gulp.src(files)
        .pipe(sass().on('error', sass.logError))
        .pipe(autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }))
        .pipe(concat('bundle-scss.css'))
        .pipe(gulp.dest('timestrap/static/css/'));
});
