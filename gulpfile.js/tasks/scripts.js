const gulp = require('gulp');

const webpack = require('webpack');
const webpackStream = require('webpack-stream');

const webpackConfig = require('../../webpack.config.js');


gulp.task('scripts', () => {
  const production = process.argv.indexOf('--production');
  if (production !== -1) webpackConfig.mode = 'production';
  return gulp.src('client/static_src/main.js')
    .pipe(webpackStream(webpackConfig, webpack))
    .on('error', function handleError() {
      this.emit('end');
    })
    .pipe(gulp.dest('client/static/'));
});
