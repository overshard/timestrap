const gulp = require('gulp');

const eslint = require('gulp-eslint');

const spawn  = require('child_process').spawn;


gulp.task('lint', ['lint:python', 'lint:es']);


gulp.task('lint:python', function(cb) {
  spawn(
    'pipenv',
    [
      'run',
      'flake8',
      '--exclude=node_modules,migrations',
    ],
    {
      stdio: 'inherit',
    }
  ).on('exit', cb);
});


gulp.task('lint:es', function() {
  return gulp.src([
    'gulpfile.js/**/*.js',
    'client/static_src/**/*.js',
    'client/static_src/components/**/*.vue'])
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(eslint.failAfterError());
});
