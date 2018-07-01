const gulp = require('gulp');

const spawn = require('child_process').spawn;


gulp.task('coverage:test', gulp.series('build:webpack:production', cb => {
  return spawn(
    'pipenv',
    ['run', 'coverage', 'run', '--source=conf,core,api', 'manage.py', 'test'],
    {stdio: 'inherit'}
  ).on('exit', code => {
    if (code !== 0) process.exit(code);
    return cb;
  });
}));


gulp.task('coverage:report', () => {
  return spawn(
    'pipenv',
    ['run', 'coverage', 'report', '-m'],
    {stdio: 'inherit'}
  );
});


gulp.task('coverage', gulp.series('lint', 'coverage:test', 'coverage:report'));
