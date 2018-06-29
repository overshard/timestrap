const gulp = require('gulp');

const concat = require('gulp-concat');

const webpack = require('webpack');
const webpackStream = require('webpack-stream');

const scriptsFiles = require('../../gulpfile.json').scriptsFiles;


gulp.task('scripts', ['scripts:vendor', 'scripts:app']);


gulp.task('scripts:vendor', () => {
    return gulp.src(scriptsFiles)
        .pipe(concat('bundle-vendor.js'))
        .pipe(gulp.dest('client/static/js/'));
});


gulp.task('scripts:app', () => {
    gulp.src('client/static_src/main.js')
        .pipe(webpackStream(require('../../webpack.config.js'), webpack))
        .pipe(concat('bundle-app.js'))
        .pipe(gulp.dest('client/static/js/'));
});
