const gulp = require('gulp');

const eslint = require('gulp-eslint');

const spawn  = require('child_process').spawn;


gulp.task('lint:python', cb => {
  return spawn(
    'pipenv',
    ['run', 'flake8', '--exclude=node_modules,migrations'],
    {stdio: 'inherit'}
  ).on('exit', code => {
    if (code !== 0) process.exit(code);
    return cb;
  });
});


gulp.task('lint:es', () => {
  return gulp.src(['gulpfile.js/**/*.js', 'client/static_src/**/*.(js|vue)'])
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(eslint.failAfterError());
});


gulp.task('lint', gulp.series('lint:python', 'lint:es'));
