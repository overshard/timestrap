const gulp = require('gulp');

const concat = require('gulp-concat');

const webpack = require('webpack');
const webpackStream = require('webpack-stream');

const webpackConfig = require('../../webpack.config.js')

const scriptsFiles = require('../../gulpfile.json').scriptsFiles;


gulp.task('scripts', ['scripts:vendor', 'scripts:app']);


gulp.task('scripts:vendor', () => {
  return gulp.src(scriptsFiles)
    .pipe(concat('bundle-vendor.js'))
    .pipe(gulp.dest('client/static/js/'));
});


gulp.task('scripts:app', () => {
  if (process.argv[3] === '--production') webpackConfig.mode = 'production';
  return gulp.src('client/static_src/main.js')
    .pipe(webpackStream(webpackConfig, webpack))
    .pipe(concat('bundle-app.js'))
    .pipe(gulp.dest('client/static/js/'));
});
