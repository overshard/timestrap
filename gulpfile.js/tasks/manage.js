const gulp = require('gulp');

const spawn = require('child_process').spawn;


gulp.task('manage:test', cb => {
  const command = ['run', 'python', 'manage.py', 'test'];

  const test = process.argv.indexOf('--test');
  if (test !== -1) command.push(process.argv[test+1]);

  const head = process.argv.indexOf('--head');
  if (head !== -1) process.env.FIREFOX_HEADLESS = 0;

  return spawn(
    'pipenv',
    command,
    {stdio: 'inherit',env: process.env}
  ).on('exit', code => {
    if (code !== 0) process.exit(code);
    return cb;
  });
});


gulp.task('manage:runserver', cb => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'runserver'],
    {stdio: 'inherit'}
  ).on('exit', code => {
    if (code !== 0) process.exit(code);
    return cb;
  });
});


gulp.task('manage:makemigrations', cb => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'makemigrations'],
    {stdio: 'inherit'}
  ).on('exit', code => {
    if (code !== 0) process.exit(code);
    return cb;
  });
});


gulp.task('manage:migrate', cb => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'migrate'],
    {stdio: 'inherit'}
  ).on('exit', code => {
    if (code !== 0) process.exit(code);
    return cb;
  });
});


gulp.task('manage:createsuperuser', cb => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'createsuperuser'],
    {stdio: 'inherit'}
  ).on('exit', code => {
    if (code !== 0) process.exit(code);
    return cb;
  });
});


gulp.task('manage:fake', cb => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'fake'],
    {stdio: 'inherit'}
  ).on('exit', code => {
    if (code !== 0) process.exit(code);
    return cb;
  });
});


gulp.task('manage:reset', cb => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'reset', '--no-input'],
    {stdio: 'inherit'}
  ).on('exit', code => {
    if (code !== 0) process.exit(code);
    return cb;
  });
});
