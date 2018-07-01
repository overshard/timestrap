const gulp = require('gulp');

const del = require('del');

const webpack = require('webpack');
const webpackStream = require('webpack-stream');

const webpackConfig = require('../../webpack.config.js');


gulp.task('build:clean', () => {
  return del([
    'client/static/**/*',
  ]);
});


gulp.task('build:webpack', () => {
  const production = process.argv.indexOf('--production');
  if (production !== -1) {
    webpackConfig.mode = 'production';
    webpackConfig.watch = false;
  }

  return gulp.src('client/static_src/main.js')
    .pipe(webpackStream(webpackConfig, webpack))
    .on('error', function handleError() {
      this.emit('end');
    })
    .pipe(gulp.dest('client/static/'));
});


gulp.task('build', gulp.series('build:clean', 'build:webpack'));
