const gulp = require('gulp');

const spawn = require('child_process').spawn;


gulp.task('manage:makemigrations', cb => {
  spawn(
    'pipenv',
    [
      'run',
      'python',
      'manage.py',
      'makemigrations',
    ],
    {
      stdio: 'inherit',
    }
  ).on('exit', cb);
});


gulp.task('manage:migrate', cb => {
  spawn(
    'pipenv',
    [
      'run',
      'python',
      'manage.py',
      'migrate',
    ],
    {
      stdio: 'inherit',
    }
  ).on('exit', cb);
});


gulp.task('manage:createsuperuser', cb => {
  spawn(
    'pipenv',
    [
      'run',
      'python',
      'manage.py',
      'createsuperuser',
    ],
    {
      stdio: 'inherit',
    }
  ).on('exit', cb);
});


gulp.task('manage:reset', cb => {
  spawn(
    'pipenv',
    [
      'run',
      'python',
      'manage.py',
      'reset',
      '--no-input',
    ],
    {
      stdio: 'inherit',
    }
  ).on('exit', cb);
});


gulp.task('manage:fake', cb => {
  spawn(
    'pipenv',
    [
      'run',
      'python',
      'manage.py',
      'fake',
    ],
    {
      stdio: 'inherit',
    }
  ).on('exit', cb);
});
