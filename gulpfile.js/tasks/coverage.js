const gulp = require('gulp');

const spawn = require('child_process').spawn;


gulp.task('coverage', cb => {
  return spawn(
    'pipenv',
    ['run', 'coverage', 'run', '--source=conf,core,api', 'manage.py', 'test'],
    {stdio: 'inherit'}
  ).on('exit', code => {
    if (code !== 0) process.exit(code);
    spawn(
      'pipenv',
      ['run', 'coverage', 'report', '-m'],
      {stdio: 'inherit'}
    ).on('exit', code => {
      if (code !== 0) process.exit(code);
      return cb;
    });
  });
});
