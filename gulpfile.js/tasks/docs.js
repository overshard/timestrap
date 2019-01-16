const gulp = require('gulp');

const spawn  = require('child_process').spawn;


gulp.task('docs:serve', () => {
  return spawn(
    'pipenv',
    ['run', 'mkdocs', 'serve'],
    {stdio: 'inherit'}
  );
});


gulp.task('docs:build', () => {
  return spawn(
    'pipenv',
    ['run', 'mkdocs', 'build'],
    {stdio: 'inherit'}
  );
});


gulp.task('docs:publish', () => {
  return spawn(
    'pipenv',
    ['run', 'mkdocs', 'gh-deploy'],
    {stdio: 'inherit'}
  );
});
