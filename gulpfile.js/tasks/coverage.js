const gulp = require('gulp');

const del = require('del');

const spawn = require('child_process').spawn;


gulp.task('coverage:test', gulp.series('build:webpack:production', () => {
  return spawn(
    'pipenv',
    ['run', 'coverage', 'run', '--source=conf,core,api', 'manage.py', 'test'],
    {stdio: 'inherit'}
  );
}));


gulp.task('coverage:report', () => {
  return spawn(
    'pipenv',
    ['run', 'coverage', 'report', '-m'],
    {stdio: 'inherit'}
  );
});


gulp.task('coverage:clean', gulp.series('build:clean', () => {
  return del([
    '.coverage',
    'geckodriver.log',
  ]);
}));


gulp.task('coverage', gulp.series('lint', 'coverage:test', 'coverage:report', 'coverage:clean'));
